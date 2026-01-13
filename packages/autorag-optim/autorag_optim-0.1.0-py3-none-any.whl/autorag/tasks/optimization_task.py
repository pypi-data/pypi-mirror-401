"""
Celery task for running optimization in the background.
Wraps existing optimization logic with progress tracking.
"""
from pathlib import Path
from typing import Dict, Any

from autorag.tasks.celery_app import app
from autorag.tasks.progress import ProgressTracker
from autorag.utils.config import load_config, DatabaseConfig
from autorag.utils.text_utils import chunk_documents, sample_chunks_for_qa
from autorag.database.supabase import SupabaseConnector
from autorag.database.mongodb import MongoDBConnector
from autorag.database.postgres import PostgreSQLConnector
from autorag.synthetic.generator import SyntheticQAGenerator
from autorag.optimization.grid_search import GridSearchOptimizer


def get_connector(config: DatabaseConfig):
    """
    Factory function to get the appropriate database connector.
    
    Args:
        config: DatabaseConfig with 'type' field
        
    Returns:
        Database connector instance (Supabase, MongoDB, or PostgreSQL)
    """
    if config.type == "supabase":
        return SupabaseConnector(config)
    elif config.type == "mongodb":
        return MongoDBConnector(config)
    elif config.type == "postgresql":
        return PostgreSQLConnector(config)
    else:
        raise ValueError(f"Unsupported database type: {config.type}")


@app.task(bind=True, name="autorag.optimize")
def run_optimization(self, config_path: str = "config.yaml", num_experiments: int = None):
    """
    Run RAG optimization as a background task.
    
    This is the Celery task version of the CLI optimize command.
    It wraps the same logic but adds progress tracking.
    
    Args:
        config_path: Path to config.yaml file
        num_experiments: Number of experiments to run (overrides config)
        
    Returns:
        Dict with optimization results and best config
    """
    # Initialize progress tracker with Celery task ID
    tracker = ProgressTracker()
    
    try:
        # ========== STEP 1: LOAD CONFIG (5%) ==========
        tracker.start(task_id=self.request.id, total_configs=9)
        tracker.update(current_step="Loading configuration", percent_complete=5)
        
        config = load_config(config_path)
        actual_experiments = num_experiments if num_experiments else config.optimization.num_experiments
        
        # Extract LLM config
        llm_provider = config.llm.provider
        llm_api_key = getattr(config.api_keys, "pi169" if llm_provider == "169pi" else llm_provider)
        llm_model = config.llm.model
        evaluation_method = config.evaluation.method
        
        # ========== STEP 2: CONNECT TO DATABASE (10%) ==========
        tracker.update(current_step="Connecting to database", percent_complete=10)
        
        # Use factory function to get the appropriate connector (supports all 3 database types)
        connector = get_connector(config.database)
        connector.test_connection()
        
        doc_count = connector.count_documents()
        if doc_count == 0:
            raise ValueError("No documents found in database")
        
        # ========== STEP 3: FETCH DOCUMENTS (15%) ==========
        tracker.update(current_step="Fetching documents", percent_complete=15)
        
        fetch_limit = min(doc_count, 100)
        documents = connector.fetch_documents(limit=fetch_limit)
        
        # ========== STEP 4: GENERATE SYNTHETIC Q&A (35%) ==========
        tracker.update(current_step="Generating synthetic Q&A pairs", percent_complete=20)
        
        # Chunk documents for diverse Q&A coverage
        all_chunks = chunk_documents(documents, chunk_size=500, chunk_overlap=50)
        
        # Randomly sample chunks for Q&A (ensures diversity)
        target_questions = config.optimization.test_questions
        sampled_chunks = sample_chunks_for_qa(all_chunks, target_questions, questions_per_chunk=1)
        
        # Initialize Q&A generator with correct params
        qa_generator = SyntheticQAGenerator(
            llm_provider=llm_provider,
            llm_api_key=llm_api_key,
            llm_model=llm_model,
            questions_per_doc=1,
            temperature=0.8
        )
        
        qa_pairs = qa_generator.generate(
            documents=sampled_chunks,
            target_count=target_questions,
            show_progress=False  # No terminal progress in background
        )
        
        # Save Q&A pairs
        output_file = Path("reports/synthetic_qa.json")
        qa_generator.save_to_file(qa_pairs, output_path=output_file)
        
        tracker.update(current_step="Q&A generation complete", percent_complete=45)
        
        # ========== STEP 5: RUN OPTIMIZATION (45% - 95%) ==========
        strategy = config.optimization.strategy
        
        # Extract RAG config for optimization
        rag_config = {
            "chunk_size": config.rag.chunk_size,
            "chunk_overlap": config.rag.chunk_overlap,
            "embedding_model": config.rag.embedding_model,
            "top_k": config.rag.top_k,
            "temperature": config.rag.temperature
        }
        
        if strategy == "bayesian":
            tracker.update(current_step="Starting Bayesian optimization (Optuna)", percent_complete=50)
            from autorag.optimization.bayesian import BayesianOptimizer
            
            optimizer = BayesianOptimizer(
                llm_provider=llm_provider,
                llm_api_key=llm_api_key,
                llm_model=llm_model,
                evaluation_method=evaluation_method,
                rag_config=rag_config,
                documents=documents
            )
            
            tracker.update(
                current_step=f"Running {actual_experiments} Bayesian trials",
                percent_complete=55,
                configs_tested=0
            )
            
            # Run Bayesian optimization
            optimizer.optimize(
                qa_pairs=qa_pairs,
                n_trials=actual_experiments,
                show_progress=False  # No terminal progress in background
            )
        else:
            # Default: Grid search
            tracker.update(current_step="Starting grid search optimization", percent_complete=50)
            
            optimizer = GridSearchOptimizer(
                llm_provider=llm_provider,
                llm_api_key=llm_api_key,
                llm_model=llm_model,
                evaluation_method=evaluation_method,
                rag_config=rag_config,
                documents=documents
            )
            
            max_configs = actual_experiments if actual_experiments <= 20 else 9
            tracker.update(
                current_step=f"Testing {max_configs} configurations",
                percent_complete=55,
                configs_tested=0
            )
            
            # Run grid search optimization
            optimizer.optimize(
                qa_pairs=qa_pairs,
                max_configs=max_configs,
                show_progress=False  # No terminal progress in background
            )
        
        # Save results
        results_file = Path("reports/optimization_results.json")
        optimizer.save_results(output_path=results_file)
        
        # ========== STEP 6: COMPLETE (100%) ==========
        best_config = optimizer.get_best_config()
        
        tracker.complete(best_config=best_config)
        
        return {
            "status": "completed",
            "best_config": best_config,
            "total_configs_tested": len(optimizer.results),
            "results_file": str(results_file),
            "qa_file": str(output_file)
        }
        
    except Exception as e:
        # Record failure in progress tracker
        tracker.fail(error_message=str(e))
        
        # Re-raise so Celery marks task as failed
        raise

"""
AutoRAG CLI - Command-line interface for RAG optimization.
"""
import json
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from pathlib import Path
from typing import Dict, Any
import typer

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


# Initialize Typer app and Rich console for beautiful terminal output
app = typer.Typer(
    name="autorag",
    help="AutoRAG Optimizer - Automatically find the optimal RAG configuration for your database",
    add_completion=False  # Disable shell completion for simplicity
)
console = Console()


@app.command()
def optimize(
    experiments: int = typer.Option(None, "--experiments", "-e", help="Number of experiments to run (overrides config)"),
    config_file: Path = typer.Option("config.yaml", "--config", "-c", help="Path to config file"),
    run_async: bool = typer.Option(False, "--async", help="Run optimization in background (requires Celery worker)")
):
    """
    Run the RAG optimization process.
    
    This will:
    1. Load your configuration
    2. Generate synthetic Q&A pairs
    3. Test multiple RAG configurations
    4. Evaluate each config using quality metrics (answer relevancy, faithfulness, etc.)
    5. Save results for analysis
    """
    console.print(Panel.fit(
        "[bold blue]AutoRAG Optimizer[/bold blue]",
        subtitle="Finding your optimal RAG configuration"
    ))
    
    # ========== LOAD & VALIDATE CONFIG ==========
    try:
        console.print(f"\n📝 Loading configuration from: [cyan]{config_file}[/cyan]")
        config = load_config(config_file)
        console.print("[green]✓[/green] Configuration loaded successfully\n")
    except FileNotFoundError as e:
        console.print(f"[bold red]❌ {e}[/bold red]")
        raise typer.Exit(code=1)
    except ValueError as e:
        console.print(f"[bold red]❌ Configuration Error:[/bold red]\n{e}")
        raise typer.Exit(code=1)
    except Exception as e:
        console.print(f"[bold red]❌ Unexpected error loading config:[/bold red]\n{e}")
        raise typer.Exit(code=1)
    
    # Override num_experiments from CLI flag if provided
    num_experiments = experiments if experiments else config.optimization.num_experiments
    
    # ========== ASYNC MODE: DISPATCH TO CELERY ==========
    if run_async:
        try:
            from autorag.tasks.optimization_task import run_optimization
            
            console.print("\n[bold cyan]🚀 Async Mode Enabled[/bold cyan]")
            console.print("  Dispatching optimization task to Celery worker...\n")
            
            # Dispatch task to Celery (non-blocking)
            task = run_optimization.delay(
                config_path=str(config_file),
                num_experiments=num_experiments
            )
            
            console.print(f"[green]✓[/green] Task dispatched successfully!")
            console.print(f"  Task ID: [cyan]{task.id}[/cyan]")
            console.print("\n[bold]Next Steps:[/bold]")
            console.print("  1. Check progress: [cyan]autorag status[/cyan]")
            console.print("  2. View results when complete: [cyan]autorag results[/cyan]")
            console.print("\n[dim]Note: Ensure Celery worker is running:[/dim]")
            console.print("  [dim]celery -A autorag.tasks.celery_app worker -Q autorag_tasks --loglevel=info[/dim]")
            return  # Exit immediately, worker handles the rest
            
        except ImportError as e:
            console.print(f"[bold red]❌ Celery not available:[/bold red] {e}")
            console.print("[dim]Install with: pip install celery redis[/dim]")
            raise typer.Exit(code=1)
        except Exception as e:
            console.print(f"[bold red]❌ Failed to dispatch async task:[/bold red] {e}")
            console.print("[dim]Is Redis running? Try: docker-compose up -d redis[/dim]")
            raise typer.Exit(code=1)
    
    # ========== DISPLAY CONFIGURATION ==========
    console.print("[bold cyan]📋 Configuration Summary[/bold cyan]")
    
    # Database info
    console.print(f"  Database: [yellow]{config.database.type}[/yellow]")
    if config.database.type == "supabase":
        console.print(f"    - URL: {config.database.url}")
        console.print(f"    - Table: {config.database.table}")
    elif config.database.type == "mongodb":
        console.print(f"    - Database: {config.database.database}")
        console.print(f"    - Collection: {config.database.collection}")
    elif config.database.type == "postgresql":
        console.print(f"    - Host: {config.database.host}:{config.database.port}")
        console.print(f"    - Database: {config.database.database}")
    
    # API keys (masked)
    console.print(f"\n  API Keys:")
    if config.api_keys.groq:
        console.print(f"    - Groq: [green]✓[/green] {config.api_keys.groq[:8]}...")
    if config.api_keys.openai:
        console.print(f"    - OpenAI: [green]✓[/green] {config.api_keys.openai[:8]}...")
    if config.api_keys.pi169:
        console.print(f"    - 169pi: [green]✓[/green] {config.api_keys.pi169[:8]}...")
    
    # Optimization settings
    console.print(f"\n  Optimization:")
    console.print(f"    - Experiments: [yellow]{num_experiments}[/yellow]")
    console.print(f"    - Test Questions: [yellow]{config.optimization.test_questions}[/yellow]")
    
    console.print("\n" + "─" * 60 + "\n")
    
    # ========== CONNECT TO DATABASE ==========
    console.print("[bold cyan]🔌 Connecting to Database[/bold cyan]")
    
    try:
        # Create connector using factory function (supports all 3 database types)
        connector = get_connector(config.database)
        
        # Test connection
        console.print("  Testing connection...", end=" ")
        connector.test_connection()
        console.print("[green]✓[/green] Connected")
        
        # Count documents
        doc_count = connector.count_documents()
        console.print(f"  Total documents: [yellow]{doc_count}[/yellow]")
        
        if doc_count == 0:
            console.print("[bold red]❌ No documents found[/bold red]")
            console.print("[dim]Please add documents to your database[/dim]")
            raise typer.Exit(code=1)
        
    except Exception as e:
        console.print(f"[bold red]❌ Database connection failed:[/bold red]\n{e}")
        raise typer.Exit(code=1)
    
    # ========== FETCH DOCUMENTS ==========
    console.print("\n[bold cyan]📚 Fetching Documents[/bold cyan]")
    
    try:
        # Fetch sample documents (limit to avoid overwhelming memory)
        fetch_limit = min(doc_count, 100)
        console.print(f"  Fetching {fetch_limit} documents...", end=" ")
        
        documents = connector.fetch_documents(limit=fetch_limit)
        console.print(f"[green]✓[/green] Fetched {len(documents)} documents")
        
        # Show sample document info
        if documents:
            sample_doc = documents[0]
            console.print(f"\n  [dim]Sample document:[/dim]")
            console.print(f"    ID: {sample_doc['id']}")
            console.print(f"    Text length: {len(sample_doc['text'])} characters")
            console.print(f"    Text preview: {sample_doc['text'][:100]}...")
            if sample_doc['metadata']:
                console.print(f"    Metadata fields: {', '.join(sample_doc['metadata'].keys())}")
        
    except Exception as e:
        console.print(f"[bold red]❌ Failed to fetch documents:[/bold red]\n{e}")
        raise typer.Exit(code=1)
    
    console.print("\n" + "─" * 60 + "\n")
    
    # ========== EXTRACT LLM CONFIG ==========
    llm_provider = config.llm.provider
    llm_api_key = getattr(config.api_keys, "pi169" if llm_provider == "169pi" else llm_provider)
    llm_model = config.llm.model
    
    # ========== DISPLAY RAG SEARCH SPACE ==========
    console.print("[bold cyan]🔧 RAG Search Space[/bold cyan]")
    
    # Extract RAG config
    rag_config = {
        "chunk_size": config.rag.chunk_size,
        "chunk_overlap": config.rag.chunk_overlap,
        "embedding_model": config.rag.embedding_model,
        "top_k": config.rag.top_k,
        "temperature": config.rag.temperature
    }
    
    # Calculate total configs
    n_indexing = len(rag_config['chunk_size']) * len(rag_config['chunk_overlap']) * len(rag_config['embedding_model'])
    n_query = len(rag_config['top_k']) * len(rag_config['temperature'])
    total_combos = n_indexing * n_query
    
    console.print(f"  [bold]Indexing Parameters:[/bold] (expensive - require re-indexing)")
    console.print(f"    chunk_size: {rag_config['chunk_size']}")
    console.print(f"    chunk_overlap: {rag_config['chunk_overlap']}")
    console.print(f"    embedding_model: {rag_config['embedding_model']}")
    console.print(f"  [bold]Query Parameters:[/bold] (fast - tested on each index)")
    console.print(f"    top_k: {rag_config['top_k']}")
    console.print(f"    temperature: {rag_config['temperature']}")
    console.print(f"  [bold]Total:[/bold] {n_indexing} indexing × {n_query} query = {total_combos} configs")
    
    console.print("\n" + "─" * 60 + "\n")
    
    # ========== GENERATE SYNTHETIC Q&A PAIRS ==========
    console.print("[bold cyan]📝 Generating Synthetic Q&A Pairs[/bold cyan]")
    
    try:
        # Step 1: Chunk documents for diverse Q&A coverage
        console.print("  Chunking documents for diversity...", end=" ")
        all_chunks = chunk_documents(documents, chunk_size=500, chunk_overlap=50)
        console.print(f"[green]✓[/green] Created {len(all_chunks)} chunks")
        
        # Step 2: Randomly sample chunks for Q&A (ensures diversity)
        target_questions = config.optimization.test_questions
        sampled_chunks = sample_chunks_for_qa(all_chunks, target_questions, questions_per_chunk=1)
        console.print(f"  Randomly sampled {len(sampled_chunks)} chunks for Q&A generation")
        
        # Step 3: Initialize Q&A generator
        qa_generator = SyntheticQAGenerator(
            llm_provider=llm_provider,
            llm_api_key=llm_api_key,
            llm_model=llm_model,
            questions_per_doc=1,  # 1 question per chunk (already sampled)
            temperature=0.8  # Higher temperature for diverse questions
        )
        
        # Step 4: Generate Q&A pairs from sampled chunks
        qa_pairs = qa_generator.generate(
            documents=sampled_chunks,  # Pass chunks as "documents"
            target_count=target_questions,
            show_progress=True
        )
        
        # Save to file
        output_file = Path("reports/synthetic_qa.json")
        qa_generator.save_to_file(qa_pairs, output_path=output_file)
        
        # Show sample Q&A pair
        if qa_pairs:
            console.print(f"\n  [dim]Sample Q&A pair:[/dim]")
            sample = qa_pairs[0]
            console.print(f"    Q: {sample['question']}")
            console.print(f"    A: {sample['answer'][:100]}...")
        
        # Show statistics
        stats = qa_generator.get_statistics()
        console.print(f"\n  [bold]Generation Statistics:[/bold]")
        console.print(f"    Total chunks used: {stats['total_documents']}")
        console.print(f"    Total questions generated: {stats['total_questions']}")
        if stats['failed_generations'] > 0:
            console.print(f"    Failed generations: [yellow]{stats['failed_generations']}[/yellow]")
        
    except Exception as e:
        console.print(f"[bold red]❌ Synthetic Q&A generation failed:[/bold red]\n{e}")
        raise typer.Exit(code=1)
    
    console.print("\n" + "─" * 60 + "\n")
    
    # ========== RUN OPTIMIZATION (Grid or Bayesian based on config) ==========
    strategy = config.optimization.strategy
    evaluation_method = config.evaluation.method
    
    try:
        if strategy == "bayesian":
            console.print("[bold cyan]🧠 Running Bayesian Optimization (Optuna)[/bold cyan]")
            console.print(f"  Evaluation Method: [yellow]{evaluation_method.upper()}[/yellow]")
            from autorag.optimization.bayesian import BayesianOptimizer
            
            optimizer = BayesianOptimizer(
                llm_provider=llm_provider,
                llm_api_key=llm_api_key,
                llm_model=llm_model,
                evaluation_method=evaluation_method,
                rag_config=rag_config,
                documents=documents
            )
            
            console.print(f"  Running {num_experiments} trials with intelligent sampling...\n")
            optimizer.optimize(
                qa_pairs=qa_pairs,
                n_trials=num_experiments,
                show_progress=True
            )
            
        else:  # Default: grid search
            console.print("[bold cyan]🔍 Running Grid Search Optimization[/bold cyan]")
            console.print(f"  Evaluation Method: [yellow]{evaluation_method.upper()}[/yellow]")
            
            optimizer = GridSearchOptimizer(
                llm_provider=llm_provider,
                llm_api_key=llm_api_key,
                llm_model=llm_model,
                evaluation_method=evaluation_method,
                rag_config=rag_config,
                documents=documents
            )
            
            console.print("  Testing multiple RAG configurations...\n")
            optimizer.optimize(
                qa_pairs=qa_pairs,
                max_configs=num_experiments if num_experiments <= 100 else 27,
                show_progress=True
            )
        
        # Save results to file (common for both strategies)
        results_file = Path("reports/optimization_results.json")
        optimizer.save_results(output_path=results_file)
        
        # Show best configuration
        best_config = optimizer.get_best_config()
        actual_eval_method = optimizer.evaluation_method
        console.print(f"\n[bold green]🏆 Optimization Complete![/bold green]")
        console.print(f"  Evaluation Method: [cyan]{actual_eval_method.upper()}[/cyan]")
        console.print(f"  Best config: [cyan]{best_config['config']['name']}[/cyan]")
        console.print(f"  Accuracy ({actual_eval_method.capitalize()} Aggregate): {best_config['metrics']['accuracy']:.3f}")
        
        # Show metric breakdown if available
        if best_config['metrics'].get('answer_relevancy') is not None:
            console.print(f"\n  [bold]{actual_eval_method.capitalize()} Metrics Breakdown:[/bold]")
            console.print(f"    • Answer Relevancy: {best_config['metrics']['answer_relevancy']:.3f}")
            console.print(f"    • Faithfulness: {best_config['metrics']['faithfulness']:.3f}")
            if best_config['metrics'].get('answer_similarity') is not None:
                console.print(f"    • Answer Similarity: {best_config['metrics']['answer_similarity']:.3f}")
            if best_config['metrics'].get('context_recall') is not None:
                console.print(f"    • Context Recall: {best_config['metrics']['context_recall']:.3f}")
        
        console.print(f"  Weighted Score: [green]{best_config['weighted_score']:.3f}[/green]")
        
    except Exception as e:
        console.print(f"[bold red]❌ Optimization failed:[/bold red]\n{e}")
        raise typer.Exit(code=1)
    
    console.print("\n" + "─" * 60 + "\n")
    
    console.print("[green]✅ AutoRAG Optimization Complete![/green]")
    console.print(f"[dim]Results saved to: {results_file}[/dim]")
    console.print(f"[dim]Q&A pairs saved to: {output_file}[/dim]")
    console.print("\n[bold]Next Steps:[/bold]")
    console.print("  1. Review results: autorag results")
    console.print("  2. Deploy best config in your production RAG system")


@app.command()
def results(
    show_report: bool = typer.Option(False, "--show-report", help="Open HTML report in browser"),
    results_file: Path = typer.Option("reports/optimization_results.json", "--file", "-f", help="Path to results file")
):
    """
    Display optimization results.
    
    Shows:
    - Best performing configurations
    - Quality metrics (answer relevancy, faithfulness, similarity, context recall)
    - Recommended configuration based on overall score
    """
    console.print(Panel.fit(
        "[bold green]📊 AutoRAG Optimization Results[/bold green]",
        subtitle="Analysis of tested configurations"
    ))
    
    # ========== LOAD RESULTS FILE ==========
    try:
        console.print(f"\n📂 Loading results from: [cyan]{results_file}[/cyan]")
        
        if not results_file.exists():
            console.print(f"[bold red]❌ Results file not found: {results_file}[/bold red]")
            console.print("[dim]Run 'autorag optimize' first to generate results.[/dim]")
            raise typer.Exit(code=1)
        
        with open(results_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        results_list = data.get("results", [])
        metadata = data.get("metadata", {})
        
        if not results_list:
            console.print("[bold red]❌ No results found in file[/bold red]")
            raise typer.Exit(code=1)
        
        console.print("[green]✓[/green] Results loaded successfully\n")
        
    except json.JSONDecodeError as e:
        console.print(f"[bold red]❌ Invalid JSON in results file:[/bold red]\n{e}")
        raise typer.Exit(code=1)
    except Exception as e:
        console.print(f"[bold red]❌ Failed to load results:[/bold red]\n{e}")
        raise typer.Exit(code=1)
    
    # ========== DISPLAY METADATA ==========
    eval_method = metadata.get('evaluation_method', 'custom')
    console.print("[bold cyan]📋 Optimization Summary[/bold cyan]")
    console.print(f"  Timestamp: {metadata.get('timestamp', 'N/A')}")
    console.print(f"  Configurations tested: [yellow]{metadata.get('total_configs_tested', 0)}[/yellow]")
    console.print(f"  Evaluation Method: [cyan]{eval_method.upper()}[/cyan]")
    
    console.print("\n" + "─" * 80 + "\n")
    
    # ========== DISPLAY RESULTS TABLE ==========
    console.print("[bold cyan]🏆 Top Configurations[/bold cyan]\n")
    
    # Create detailed results table
    table = Table(show_header=True, header_style="bold magenta", show_lines=True)
    table.add_column("Rank", style="dim", width=6, justify="center")
    table.add_column("Configuration", style="cyan")
    table.add_column(f"{eval_method.capitalize()} Score", justify="right")
    table.add_column("Success Rate", justify="right")
    table.add_column("Overall\nScore", justify="right", style="bold green")
    
    # Add all results to table
    for i, result in enumerate(results_list, 1):
        config = result["config"]
        metrics = result["metrics"]
        
        # Calculate success rate
        success_rate = (metrics["successful_queries"] / metrics["total_queries"]) * 100
        
        # Highlight best config
        rank_style = "bold yellow" if i == 1 else "dim"
        
        table.add_row(
            f"#{i}" if i > 1 else "🥇",
            f"{config['name']}\n(k={config['top_k']}, t={config['temperature']})",
            f"{metrics['accuracy']:.3f}",
            f"{success_rate:.0f}%",
            f"{result['weighted_score']:.3f}",
            style=rank_style if i == 1 else None
        )
    
    console.print(table)
    
    # ========== DISPLAY BEST CONFIGURATION DETAILS ==========
    console.print("\n" + "─" * 80 + "\n")
    
    best = results_list[0]
    console.print("[bold green]🎯 Recommended Configuration[/bold green]\n")
    
    console.print(f"  [bold]Configuration Name:[/bold] {best['config']['name']}")
    console.print(f"  [bold]Parameters:[/bold]")
    console.print(f"    • top_k: [cyan]{best['config']['top_k']}[/cyan] documents")
    console.print(f"    • temperature: [cyan]{best['config']['temperature']}[/cyan]")
    
    console.print(f"\n  [bold]Performance Metrics:[/bold]")
    console.print(f"    • {eval_method.capitalize()} Aggregate Score: [green]{best['metrics']['accuracy']:.3f}[/green]")
    console.print(f"    • Success Rate: [green]{(best['metrics']['successful_queries']/best['metrics']['total_queries'])*100:.0f}%[/green]")
    
    console.print(f"\n  [bold]Overall Score ({eval_method.capitalize()} Aggregate):[/bold] [bold green]{best['weighted_score']:.3f}[/bold green]")
    
    # ========== SHOW METRICS BREAKDOWN ==========
    if best['metrics'].get('answer_relevancy') is not None:
        console.print(f"\n  [bold]{eval_method.capitalize()} Metrics Breakdown:[/bold]")
        console.print(f"    • Answer Relevancy: [cyan]{best['metrics']['answer_relevancy']:.3f}[/cyan]")
        console.print(f"    • Faithfulness: [cyan]{best['metrics']['faithfulness']:.3f}[/cyan]")
        if best['metrics'].get('answer_similarity') is not None:
            console.print(f"    • Answer Similarity: [cyan]{best['metrics']['answer_similarity']:.3f}[/cyan]")
        if best['metrics'].get('context_recall') is not None:
            console.print(f"    • Context Recall: [cyan]{best['metrics']['context_recall']:.3f}[/cyan]")
        console.print(f"\n    [dim]Note: Overall score is the weighted average of {eval_method} metrics[/dim]")
    else:
        console.print(f"\n  [dim]Individual Ragas metrics not available (fallback mode used)[/dim]")
    
    # ========== COMPARISON WITH WORST ==========
    if len(results_list) > 1:
        worst = results_list[-1]
        console.print("\n" + "─" * 80 + "\n")
        console.print("[bold cyan]📈 Improvement over Worst Config[/bold cyan]\n")
        
        acc_improvement = ((best['metrics']['accuracy'] - worst['metrics']['accuracy']) / worst['metrics']['accuracy']) * 100
        
        console.print(f"  Accuracy: [green]{acc_improvement:+.1f}%[/green]")
    
    # ========== GENERATE HTML REPORT (OPTIONAL) ==========
    if show_report:
        console.print("\n" + "─" * 80 + "\n")
        console.print("[bold cyan]📄 Generating HTML Report[/bold cyan]\n")
        
        try:
            html_path = _generate_html_report(data, results_file.parent)
            console.print(f"[green]✓[/green] HTML report generated: {html_path}")
            
            # Open in browser
            import webbrowser
            webbrowser.open(f"file://{html_path.absolute()}")
            console.print("[green]✓[/green] Opened in default browser")
            
        except Exception as e:
            console.print(f"[yellow]⚠️  Failed to generate HTML report: {e}[/yellow]")
    
    console.print("\n" + "─" * 80 + "\n")
    console.print("[bold]💡 Next Steps:[/bold]")
    console.print(f"  1. Use the best config (k={best['config']['top_k']}, temp={best['config']['temperature']}) in your RAG system")
    console.print("  2. Run 'autorag optimize' again with different parameters to explore more configs")
    console.print("  3. Use '--show-report' flag to see detailed HTML report")


def _format_metrics_breakdown_html(metrics: Dict[str, Any], eval_method: str) -> str:
    """
    Format metrics breakdown as visual progress bars for HTML report.
    
    Args:
        metrics: Metrics dict containing scores
        eval_method: Evaluation method name
        
    Returns:
        HTML string with metrics breakdown or empty string if not available
    """
    if metrics.get('answer_relevancy') is not None:
        def get_bar_class(value: float) -> str:
            if value >= 0.8:
                return "high"
            elif value >= 0.5:
                return ""
            return "medium"
        
        context_recall = metrics.get('context_recall', 0)
        faithfulness = metrics.get('faithfulness', 0)
        answer_relevancy = metrics.get('answer_relevancy', 0)
        answer_similarity = metrics.get('answer_similarity', 0)
        
        breakdown = f'''
            <div class="metrics-breakdown">
                <h3>{eval_method.capitalize()} Metrics Breakdown</h3>
                
                <div class="metric-bar-container">
                    <div class="metric-bar-header">
                        <span class="metric-bar-label">Context Recall</span>
                        <span class="metric-bar-value">{context_recall:.3f}</span>
                    </div>
                    <div class="metric-bar">
                        <div class="metric-bar-fill {get_bar_class(context_recall)}" style="width: {context_recall * 100:.1f}%;"></div>
                    </div>
                </div>

                <div class="metric-bar-container">
                    <div class="metric-bar-header">
                        <span class="metric-bar-label">Faithfulness</span>
                        <span class="metric-bar-value">{faithfulness:.3f}</span>
                    </div>
                    <div class="metric-bar">
                        <div class="metric-bar-fill {get_bar_class(faithfulness)}" style="width: {faithfulness * 100:.1f}%;"></div>
                    </div>
                </div>

                <div class="metric-bar-container">
                    <div class="metric-bar-header">
                        <span class="metric-bar-label">Answer Relevancy</span>
                        <span class="metric-bar-value">{answer_relevancy:.3f}</span>
                    </div>
                    <div class="metric-bar">
                        <div class="metric-bar-fill {get_bar_class(answer_relevancy)}" style="width: {answer_relevancy * 100:.1f}%;"></div>
                    </div>
                </div>

                <div class="metric-bar-container">
                    <div class="metric-bar-header">
                        <span class="metric-bar-label">Answer Similarity</span>
                        <span class="metric-bar-value">{answer_similarity:.3f}</span>
                    </div>
                    <div class="metric-bar">
                        <div class="metric-bar-fill {get_bar_class(answer_similarity)}" style="width: {answer_similarity * 100:.1f}%;"></div>
                    </div>
                </div>
            </div>
        '''
        return breakdown
    return ""


def _generate_html_report(data: Dict[str, Any], output_dir: Path) -> Path:
    """
    Generate a professional HTML report from optimization results.
    
    Args:
        data: Results data dict
        output_dir: Directory to save HTML report
        
    Returns:
        Path to generated HTML file
    """
    html_path = output_dir / "optimization_report.html"
    
    results_list = data.get("results", [])
    metadata = data.get("metadata", {})
    eval_method = metadata.get('evaluation_method', 'custom')
    total_configs = metadata.get('total_configs_tested', len(results_list))
    timestamp = metadata.get('timestamp', 'N/A')
    
    # Calculate improvement percentage
    if len(results_list) > 1 and results_list[-1]['weighted_score'] > 0:
        improvement = ((results_list[0]['weighted_score'] - results_list[-1]['weighted_score']) / results_list[-1]['weighted_score']) * 100
    else:
        improvement = 0
    
    best_config = results_list[0] if results_list else {}
    best_score = best_config.get('weighted_score', 0)
    best_name = best_config.get('config', {}).get('name', 'N/A')
    best_k = best_config.get('config', {}).get('top_k', 'N/A')
    best_temp = best_config.get('config', {}).get('temperature', 'N/A')
    
    # Professional HTML template
    html_content = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AutoRAG Optimization Report</title>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">
    <style>
        :root {{
            --primary-gradient: linear-gradient(135deg, #0d9488 0%, #14b8a6 50%, #2dd4bf 100%);
            --secondary-gradient: linear-gradient(135deg, #0891b2 0%, #06b6d4 100%);
            --bg-color: #0f172a;
            --surface-color: #1e293b;
            --text-primary: #f1f5f9;
            --text-secondary: #94a3b8;
            --text-muted: #64748b;
            --border-color: rgba(255, 255, 255, 0.08);
            --success-color: #10b981;
        }}

        * {{ margin: 0; padding: 0; box-sizing: border-box; }}

        body {{
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: var(--bg-color);
            min-height: 100vh;
            color: var(--text-primary);
            line-height: 1.6;
        }}

        .bg-pattern {{
            position: fixed;
            inset: 0;
            background: 
                radial-gradient(circle at 20% 20%, rgba(20, 184, 166, 0.12) 0%, transparent 40%),
                radial-gradient(circle at 80% 80%, rgba(6, 182, 212, 0.08) 0%, transparent 40%);
            pointer-events: none;
            z-index: 0;
        }}

        .container {{
            max-width: 1200px;
            margin: 0 auto;
            padding: 40px 24px;
            position: relative;
            z-index: 1;
        }}

        .header {{
            background: var(--primary-gradient);
            border-radius: 24px;
            padding: 48px;
            margin-bottom: 32px;
            position: relative;
            overflow: hidden;
            box-shadow: 0 20px 40px -12px rgba(20, 184, 166, 0.35);
        }}

        .header::before {{
            content: '';
            position: absolute;
            top: 0;
            right: 0;
            width: 400px;
            height: 400px;
            background: radial-gradient(circle, rgba(255, 255, 255, 0.1) 0%, transparent 70%);
            transform: translate(30%, -30%);
        }}

        .header-content {{ position: relative; z-index: 1; }}

        .header-badge {{
            display: inline-flex;
            align-items: center;
            gap: 8px;
            background: rgba(255, 255, 255, 0.2);
            backdrop-filter: blur(10px);
            padding: 8px 16px;
            border-radius: 100px;
            font-size: 13px;
            font-weight: 500;
            margin-bottom: 20px;
            border: 1px solid rgba(255, 255, 255, 0.2);
        }}

        .header h1 {{
            font-size: 42px;
            font-weight: 700;
            margin-bottom: 12px;
            letter-spacing: -0.02em;
        }}

        .header-meta {{
            display: flex;
            flex-wrap: wrap;
            gap: 24px;
            margin-top: 20px;
            font-size: 14px;
            opacity: 0.9;
        }}

        .stats-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            margin-bottom: 32px;
        }}

        .stat-card {{
            background: var(--surface-color);
            border-radius: 16px;
            padding: 24px;
            border: 1px solid var(--border-color);
            transition: all 0.3s ease;
        }}

        .stat-card:hover {{
            transform: translateY(-4px);
            box-shadow: 0 12px 32px -8px rgba(0, 0, 0, 0.4);
        }}

        .stat-label {{
            font-size: 13px;
            text-transform: uppercase;
            letter-spacing: 0.05em;
            color: var(--text-muted);
            margin-bottom: 8px;
        }}

        .stat-value {{
            font-size: 32px;
            font-weight: 700;
            background: var(--primary-gradient);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }}

        .stat-subtext {{
            font-size: 12px;
            color: var(--text-secondary);
            margin-top: 4px;
        }}

        .card {{
            background: var(--surface-color);
            border-radius: 24px;
            padding: 32px;
            margin-bottom: 32px;
            border: 1px solid var(--border-color);
            position: relative;
            overflow: hidden;
        }}

        .card::before {{
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 4px;
            background: var(--secondary-gradient);
        }}

        .section-header {{
            display: flex;
            align-items: center;
            gap: 12px;
            margin-bottom: 24px;
        }}

        .section-header h2 {{
            font-size: 24px;
            font-weight: 600;
        }}

        .section-header span {{ font-size: 28px; }}

        .config-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
            gap: 24px;
        }}

        .config-detail {{
            background: rgba(255, 255, 255, 0.03);
            border-radius: 12px;
            padding: 20px;
            border: 1px solid var(--border-color);
        }}

        .config-detail-label {{
            font-size: 12px;
            text-transform: uppercase;
            letter-spacing: 0.05em;
            color: var(--text-muted);
            margin-bottom: 8px;
        }}

        .config-detail-value {{
            font-size: 18px;
            font-weight: 600;
        }}

        .score-highlight {{
            background: var(--secondary-gradient);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            font-size: 48px;
            font-weight: 700;
        }}

        .metrics-breakdown {{
            margin-top: 24px;
            padding-top: 24px;
            border-top: 1px solid var(--border-color);
        }}

        .metrics-breakdown h3 {{
            font-size: 16px;
            font-weight: 600;
            margin-bottom: 16px;
            color: var(--text-secondary);
        }}

        .metric-bar-container {{ margin-bottom: 16px; }}

        .metric-bar-header {{
            display: flex;
            justify-content: space-between;
            margin-bottom: 8px;
            font-size: 14px;
        }}

        .metric-bar-label {{ color: var(--text-secondary); }}
        .metric-bar-value {{ font-weight: 600; }}

        .metric-bar {{
            height: 8px;
            background: rgba(255, 255, 255, 0.1);
            border-radius: 100px;
            overflow: hidden;
        }}

        .metric-bar-fill {{
            height: 100%;
            border-radius: 100px;
            background: var(--primary-gradient);
            transition: width 0.8s ease;
        }}

        .metric-bar-fill.high {{ background: var(--secondary-gradient); }}
        .metric-bar-fill.medium {{ background: linear-gradient(135deg, #f59e0b 0%, #fbbf24 100%); }}

        .table-container {{ overflow-x: auto; }}

        table {{
            width: 100%;
            border-collapse: separate;
            border-spacing: 0;
        }}

        thead th {{
            background: rgba(20, 184, 166, 0.2);
            color: var(--text-primary);
            font-weight: 600;
            font-size: 13px;
            text-transform: uppercase;
            letter-spacing: 0.05em;
            padding: 16px 20px;
            text-align: left;
            border-bottom: 1px solid var(--border-color);
        }}

        thead th:first-child {{ border-radius: 12px 0 0 0; }}
        thead th:last-child {{ border-radius: 0 12px 0 0; }}

        tbody td {{
            padding: 16px 20px;
            border-bottom: 1px solid var(--border-color);
            font-size: 14px;
            color: var(--text-secondary);
        }}

        tbody tr:hover {{ background: rgba(20, 184, 166, 0.08); }}
        tbody tr:hover td {{ color: var(--text-primary); }}
        tbody tr:last-child td {{ border-bottom: none; }}
        tbody tr.best-row {{ background: rgba(16, 185, 129, 0.1); }}
        tbody tr.best-row td {{ color: var(--text-primary); font-weight: 500; }}

        .rank-badge {{
            display: inline-flex;
            align-items: center;
            justify-content: center;
            width: 32px;
            height: 32px;
            border-radius: 8px;
            font-weight: 600;
            font-size: 13px;
        }}

        .rank-1 {{ background: linear-gradient(135deg, #fbbf24 0%, #f59e0b 100%); color: #1a1a2e; }}
        .rank-2 {{ background: linear-gradient(135deg, #94a3b8 0%, #64748b 100%); color: #1a1a2e; }}
        .rank-3 {{ background: linear-gradient(135deg, #c2410c 0%, #ea580c 100%); color: white; }}
        .rank-default {{ background: rgba(255, 255, 255, 0.1); color: var(--text-secondary); }}

        .config-name {{ font-weight: 500; color: var(--text-primary); }}
        .config-params {{ font-size: 12px; color: var(--text-muted); margin-top: 4px; }}

        .score-pill {{
            display: inline-block;
            padding: 6px 12px;
            border-radius: 100px;
            font-weight: 600;
            font-size: 14px;
            background: rgba(16, 185, 129, 0.15);
            color: var(--success-color);
        }}

        .recommendation-list {{ list-style: none; }}

        .recommendation-item {{
            display: flex;
            align-items: flex-start;
            gap: 16px;
            padding: 16px 0;
            border-bottom: 1px solid var(--border-color);
        }}

        .recommendation-item:last-child {{ border-bottom: none; padding-bottom: 0; }}

        .recommendation-icon {{
            width: 40px;
            height: 40px;
            border-radius: 12px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 20px;
            background: rgba(20, 184, 166, 0.15);
            flex-shrink: 0;
        }}

        .recommendation-content h4 {{ font-size: 15px; font-weight: 600; margin-bottom: 4px; }}
        .recommendation-content p {{ font-size: 14px; color: var(--text-secondary); }}

        .footer {{
            text-align: center;
            padding: 40px 0;
            color: var(--text-muted);
            font-size: 13px;
        }}

        .footer a {{ color: #14b8a6; text-decoration: none; }}
        .footer a:hover {{ text-decoration: underline; }}

        @keyframes fadeInUp {{
            from {{ opacity: 0; transform: translateY(20px); }}
            to {{ opacity: 1; transform: translateY(0); }}
        }}

        .header, .stats-grid, .card {{ animation: fadeInUp 0.6s ease-out forwards; }}

        @media (max-width: 768px) {{
            .container {{ padding: 20px 16px; }}
            .header {{ padding: 32px 24px; }}
            .header h1 {{ font-size: 28px; }}
            .score-highlight {{ font-size: 36px; }}
        }}
    </style>
</head>
<body>
    <div class="bg-pattern"></div>
    
    <div class="container">
        <header class="header">
            <div class="header-content">
                <div class="header-badge">📊 Evaluation Method: {eval_method.upper()}</div>
                <h1>🎯 AutoRAG Optimization Report</h1>
                <div class="header-meta">
                    <span>📅 Generated: {timestamp}</span>
                    <span>🔬 {total_configs} Configurations Tested</span>
                </div>
            </div>
        </header>

        <div class="stats-grid">
            <div class="stat-card">
                <div class="stat-label">Best Score</div>
                <div class="stat-value">{best_score:.3f}</div>
                <div class="stat-subtext">{eval_method.capitalize()} Aggregate</div>
            </div>
            <div class="stat-card">
                <div class="stat-label">Configs Tested</div>
                <div class="stat-value">{total_configs}</div>
                <div class="stat-subtext">Total experiments</div>
            </div>
            <div class="stat-card">
                <div class="stat-label">Improvement</div>
                <div class="stat-value">{improvement:+.1f}%</div>
                <div class="stat-subtext">vs. worst config</div>
            </div>
            <div class="stat-card">
                <div class="stat-label">Top Parameters</div>
                <div class="stat-value">k={best_k}, t={best_temp}</div>
                <div class="stat-subtext">Optimal settings</div>
            </div>
        </div>

        <div class="card">
            <div class="section-header">
                <span>🏆</span>
                <h2>Best Configuration</h2>
            </div>
            
            <div class="config-grid">
                <div class="config-detail">
                    <div class="config-detail-label">Configuration Name</div>
                    <div class="config-detail-value">{best_name}</div>
                </div>
                <div class="config-detail">
                    <div class="config-detail-label">Top K Documents</div>
                    <div class="config-detail-value">{best_k}</div>
                </div>
                <div class="config-detail">
                    <div class="config-detail-label">Temperature</div>
                    <div class="config-detail-value">{best_temp}</div>
                </div>
                <div class="config-detail">
                    <div class="config-detail-label">Overall Score</div>
                    <div class="score-highlight">{best_score:.3f}</div>
                </div>
            </div>
            {_format_metrics_breakdown_html(best_config.get('metrics', {}), eval_method)}
        </div>

        <div class="card">
            <div class="section-header">
                <span>📊</span>
                <h2>All Configurations</h2>
            </div>
            
            <div class="table-container">
                <table>
                    <thead>
                        <tr>
                            <th>Rank</th>
                            <th>Configuration</th>
                            <th>Overall Score</th>
                            <th>Answer Relevancy</th>
                            <th>Faithfulness</th>
                            <th>Answer Similarity</th>
                            <th>Context Recall</th>
                        </tr>
                    </thead>
                    <tbody>
'''
    
    # Add table rows with metrics for each config
    for i, result in enumerate(results_list, 1):
        row_class = "best-row" if i == 1 else ""
        if i == 1:
            rank_class = "rank-1"
        elif i == 2:
            rank_class = "rank-2"
        elif i == 3:
            rank_class = "rank-3"
        else:
            rank_class = "rank-default"
        
        config_name = result['config']['name']
        config_k = result['config']['top_k']
        config_t = result['config']['temperature']
        weighted_score = result['weighted_score']
        metrics = result.get('metrics', {})
        
        # Get individual metrics with fallback to 0
        answer_relevancy = metrics.get('answer_relevancy') or 0
        faithfulness = metrics.get('faithfulness') or 0
        answer_similarity = metrics.get('answer_similarity') or 0
        context_recall = metrics.get('context_recall') or 0
        
        html_content += f'''
                        <tr class="{row_class}">
                            <td><span class="rank-badge {rank_class}">{i}</span></td>
                            <td>
                                <div class="config-name">{config_name}</div>
                                <div class="config-params">k={config_k}, t={config_t}</div>
                            </td>
                            <td><span class="score-pill">{weighted_score:.3f}</span></td>
                            <td>{answer_relevancy:.3f}</td>
                            <td>{faithfulness:.3f}</td>
                            <td>{answer_similarity:.3f}</td>
                            <td>{context_recall:.3f}</td>
                        </tr>
'''

    
    html_content += '''
                    </tbody>
                </table>
            </div>
        </div>

        <div class="card">
            <div class="section-header">
                <span>💡</span>
                <h2>Recommendations</h2>
            </div>
            
            <ul class="recommendation-list">
                <li class="recommendation-item">
                    <div class="recommendation-icon">🚀</div>
                    <div class="recommendation-content">
                        <h4>Deploy Best Configuration</h4>
                        <p>Use the winning configuration in your production RAG system for optimal performance.</p>
                    </div>
                </li>
                <li class="recommendation-item">
                    <div class="recommendation-icon">📈</div>
                    <div class="recommendation-content">
                        <h4>Monitor Performance</h4>
                        <p>Track real-world accuracy and response quality metrics after deployment.</p>
                    </div>
                </li>
                <li class="recommendation-item">
                    <div class="recommendation-icon">🔄</div>
                    <div class="recommendation-content">
                        <h4>Periodic Re-optimization</h4>
                        <p>Run optimization again when your document base grows significantly or user query patterns change.</p>
                    </div>
                </li>
            </ul>
        </div>
        
        <footer class="footer">
            <p>Generated by AutoRAG Optimizer</p>
        </footer>
    </div>
</body>
</html>
'''
    
    # Write HTML file
    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    return html_path


@app.command()
def status(
    config_file: Path = typer.Option("config.yaml", "--config", "-c", help="Path to config file")
):
    """
    Check the status of running optimization.
    
    Shows:
    - Current progress (experiments completed)
    - Estimated time remaining
    - Best configuration so far
    """
    from autorag.tasks.progress import ProgressTracker
    from rich.progress import Progress, BarColumn, TextColumn, TaskProgressColumn
    
    console.print(Panel.fit(
        "[bold cyan]📊 Optimization Status[/bold cyan]",
        subtitle="Background task progress"
    ))
    
    # Load progress from file
    tracker = ProgressTracker()
    progress = tracker.load()
    
    if progress is None:
        console.print("\n[yellow]⚠️  No optimization in progress[/yellow]")
        console.print("[dim]Run 'autorag optimize --async' to start a background optimization[/dim]")
        return
    
    # Display task info
    console.print(f"\n[bold]Task ID:[/bold] [cyan]{progress.task_id}[/cyan]")
    console.print(f"[bold]Status:[/bold] ", end="")
    
    # Color-coded status
    if progress.status == "running":
        console.print("[blue]🔄 Running[/blue]")
    elif progress.status == "completed":
        console.print("[green]✅ Completed[/green]")
    elif progress.status == "failed":
        console.print("[red]❌ Failed[/red]")
    else:
        console.print(f"[yellow]{progress.status}[/yellow]")
    
    # Timestamps
    if progress.started_at:
        console.print(f"[bold]Started:[/bold] {progress.started_at}")
    if progress.completed_at:
        console.print(f"[bold]Completed:[/bold] {progress.completed_at}")
    
    console.print("\n" + "─" * 60 + "\n")
    
    # Progress bar
    console.print(f"[bold]Current Step:[/bold] {progress.current_step}")
    console.print(f"[bold]Progress:[/bold] {progress.percent_complete}%")
    
    # Visual progress bar using Rich
    with Progress(
        TextColumn("[progress.description]{task.description}"),
        BarColumn(bar_width=40),
        TaskProgressColumn(),
        console=console,
        transient=True
    ) as progress_bar:
        task = progress_bar.add_task("Optimization", total=100, completed=progress.percent_complete)
        progress_bar.refresh()
    
    # Configs tested
    if progress.total_configs > 0:
        console.print(f"\n[bold]Configurations:[/bold] {progress.configs_tested}/{progress.total_configs} tested")
    
    # Best config so far
    if progress.best_config_so_far:
        console.print("\n" + "─" * 60)
        console.print("\n[bold green]🏆 Best Configuration So Far[/bold green]")
        config = progress.best_config_so_far
        
        if isinstance(config, dict):
            if "config" in config:
                console.print(f"  Name: [cyan]{config['config'].get('name', 'N/A')}[/cyan]")
                console.print(f"  top_k: {config['config'].get('top_k', 'N/A')}")
                console.print(f"  temperature: {config['config'].get('temperature', 'N/A')}")
            if "metrics" in config:
                console.print(f"  Accuracy: [green]{config['metrics'].get('accuracy', 0):.3f}[/green]")
            if "weighted_score" in config:
                console.print(f"  Weighted Score: [green]{config.get('weighted_score', 0):.3f}[/green]")
    
    # Error message if failed
    if progress.status == "failed" and progress.error_message:
        console.print("\n" + "─" * 60)
        console.print("\n[bold red]Error Details:[/bold red]")
        console.print(f"  {progress.error_message}")
    
    # Next steps
    console.print("\n" + "─" * 60 + "\n")
    if progress.status == "running":
        console.print("[bold]💡 Tip:[/bold] Run 'autorag status' again to see updated progress")
    elif progress.status == "completed":
        console.print("[bold]Next:[/bold] Run 'autorag results' to see full results")


# Entry point for the CLI
if __name__ == "__main__":
    app()

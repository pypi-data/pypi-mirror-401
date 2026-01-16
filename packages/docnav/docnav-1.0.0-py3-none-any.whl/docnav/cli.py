# CLI interface
"""
Command-line interface for DocNav.
"""

import os
import sys
import json
from pathlib import Path
from typing import Optional, List
import argparse
from datetime import datetime

from rich.console import Console
from rich.table import Table
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.panel import Panel
from rich.markdown import Markdown
from rich.syntax import Syntax
from rich import print as rprint

from .core import DocCorpus, ask

console = Console()

def main():
    parser = argparse.ArgumentParser(description="DocNav: AI-powered document querying with citations")
    subparsers = parser.add_subparsers(dest="command", help="Commands")
    
    # Create command
    create_parser = subparsers.add_parser("create", help="Create a new document corpus")
    create_parser.add_argument("name", help="Name of the corpus")
    create_parser.add_argument("--path", help="Path to store corpus", default="./.docnav")
    create_parser.add_argument("--embedding-model", default="all-MiniLM-L6-v2", 
                              help="Embedding model to use")
    
    # Add command
    add_parser = subparsers.add_parser("add", help="Add documents to corpus")
    add_parser.add_argument("corpus", help="Corpus name or path")
    add_parser.add_argument("paths", nargs="+", help="Files or directories to add")
    add_parser.add_argument("--use-ocr", action="store_true", help="Use OCR for scanned PDFs")
    add_parser.add_argument("--chunk-size", type=int, default=1000, help="Chunk size in tokens")
    add_parser.add_argument("--update", action="store_true", 
                           help="Update existing documents")
    
    # Ask command
    ask_parser = subparsers.add_parser("ask", help="Ask a question to corpus")
    ask_parser.add_argument("corpus", help="Corpus name or path")
    ask_parser.add_argument("query", help="Question to ask")
    ask_parser.add_argument("--llm-provider", choices=["openai", "gemini"], 
                           default="openai", help="LLM provider to use")
    ask_parser.add_argument("--llm-model", help="LLM model name")
    ask_parser.add_argument("--api-key", help="API key for LLM provider")
    ask_parser.add_argument("--top-k", type=int, default=5, help="Number of chunks to consider")
    ask_parser.add_argument("--temperature", type=float, help="Temperature for generation")
    ask_parser.add_argument("--where", help="Filter query (JSON format)")
    
    # List command
    list_parser = subparsers.add_parser("list", help="List documents in corpus")
    list_parser.add_argument("corpus", help="Corpus name or path")
    
    # Stats command
    stats_parser = subparsers.add_parser("stats", help="Get corpus statistics")
    stats_parser.add_argument("corpus", help="Corpus name or path")
    
    # Remove command
    remove_parser = subparsers.add_parser("remove", help="Remove document from corpus")
    remove_parser.add_argument("corpus", help="Corpus name or path")
    remove_parser.add_argument("file", help="File to remove")
    
    # Clear command
    clear_parser = subparsers.add_parser("clear", help="Clear entire corpus")
    clear_parser.add_argument("corpus", help="Corpus name or path")
    
    # Quick ask command (one-liner)
    quick_ask_parser = subparsers.add_parser("quick-ask", help="Quickly ask a document")
    quick_ask_parser.add_argument("file", help="Document file")
    quick_ask_parser.add_argument("query", help="Question to ask")
    quick_ask_parser.add_argument("--api-key", help="API key")
    quick_ask_parser.add_argument("--provider", choices=["openai", "gemini"], 
                                 default="openai", help="LLM provider")
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    try:
        if args.command == "create":
            handle_create(args)
        elif args.command == "add":
            handle_add(args)
        elif args.command == "ask":
            handle_ask(args)
        elif args.command == "list":
            handle_list(args)
        elif args.command == "stats":
            handle_stats(args)
        elif args.command == "remove":
            handle_remove(args)
        elif args.command == "clear":
            handle_clear(args)
        elif args.command == "quick-ask":
            handle_quick_ask(args)
            
    except Exception as e:
        console.print(f"[bold red]Error:[/bold red] {e}", style="red")
        sys.exit(1)

def handle_create(args):
    """Handle create command."""
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        transient=True,
    ) as progress:
        progress.add_task(description="Creating corpus...", total=None)
        
        corpus = DocCorpus(
            corpus_path=args.path,
            embedding_model=args.embedding_model
        )
    
    console.print(f"[green]✓[/green] Corpus created at: {args.path}")
    console.print(f"[green]✓[/green] Embedding Model: {args.embedding_model}")

def handle_add(args):
    """Handle add command."""
    corpus = load_corpus(args.corpus)
    
    with Progress() as progress:
        task = progress.add_task("Adding documents...", total=None)
        
        added = corpus.add_documents(
            args.paths,
            use_ocr=args.use_ocr,
            chunk_size=args.chunk_size,
            update_existing=args.update
        )
        
        progress.update(task, completed=True)
    
    console.print(f"[green]✓[/green] Added {added} new chunks to corpus")

def handle_ask(args):
    """Handle ask command."""
    # Get API key from argument or environment
    api_key = args.api_key or os.getenv(f"{args.llm_provider.upper()}_API_KEY")
    
    if not api_key:
        console.print(f"[red]Error:[/red] API key required for {args.llm_provider}")
        console.print(f"Set {args.llm_provider.upper()}_API_KEY environment variable or use --api-key")
        return
    
    corpus = load_corpus(args.corpus)
    
    # Parse where filter
    where_filter = None
    if args.where:
        try:
            where_filter = json.loads(args.where)
        except json.JSONDecodeError:
            console.print("[yellow]Warning:[/yellow] Invalid JSON for --where filter, ignoring")
    
    with Progress() as progress:
        task = progress.add_task("Searching and generating answer...", total=None)
        
        result = corpus.ask(
            query=args.query,
            llm_provider=args.llm_provider,
            llm_model=args.llm_model,
            api_key=api_key,
            top_k=args.top_k,
            where=where_filter,
            temperature=args.temperature
        )
        
        progress.update(task, completed=True)
    
    # Display answer
    console.print("\n")
    console.print(Panel.fit(
        Markdown(result.answer.text),
        title="[bold blue]Answer[/bold blue]",
        border_style="blue"
    ))
    
    # Display metadata
    table = Table(title="Answer Details")
    table.add_column("Metric", style="cyan")
    table.add_column("Value", style="white")
    
    table.add_row("Confidence", f"{result.answer.confidence:.2%}")
    table.add_row("Processing Time", f"{result.processing_time:.2f}s")
    table.add_row("Chunks Considered", str(result.total_chunks_considered))
    table.add_row("Model Used", result.model_used)
    
    console.print(table)
    
    # Display sources
    if result.answer.sources:
        console.print("\n[bold green]Sources:[/bold green]")
        for i, source in enumerate(result.answer.sources, 1):
            meta = source.metadata
            source_text = f"[cyan]{i}. {meta.get('file_name', 'Unknown')}[/cyan]"
            
            if 'page' in meta:
                source_text += f" [yellow](Page {meta['page']})[/yellow]"
            
            if 'type' in meta:
                source_text += f" [dim]{meta['type'].upper()}[/dim]"
            
            console.print(source_text)
            
            # Show snippet
            snippet = source.text[:200] + "..." if len(source.text) > 200 else source.text
            console.print(f"   [dim]{snippet}[/dim]")
            console.print()

def handle_list(args):
    """Handle list command."""
    corpus = load_corpus(args.corpus)
    documents = corpus.list_documents()
    
    if not documents:
        console.print("[yellow]No documents in corpus[/yellow]")
        return
    
    table = Table(title=f"Documents in Corpus ({len(documents)})")
    table.add_column("#", style="dim")
    table.add_column("File", style="cyan")
    table.add_column("Type", style="green")
    table.add_column("Chunks", style="yellow", justify="right")
    table.add_column("Path", style="dim")
    
    for i, doc in enumerate(documents, 1):
        table.add_row(
            str(i),
            doc['file_name'],
            doc['type'],
            str(doc['chunk_count']),
            doc['file_path']
        )
    
    console.print(table)

def handle_stats(args):
    """Handle stats command."""
    corpus = load_corpus(args.corpus)
    stats = corpus.get_stats()
    
    table = Table(title="Corpus Statistics")
    table.add_column("Metric", style="cyan")
    table.add_column("Value", style="white")
    
    for key, value in stats.items():
        table.add_row(key.replace('_', ' ').title(), str(value))
    
    console.print(table)

def handle_remove(args):
    """Handle remove command."""
    corpus = load_corpus(args.corpus)
    removed = corpus.remove_document(args.file)
    
    if removed > 0:
        console.print(f"[green]✓[/green] Removed {removed} chunks for {args.file}")
    else:
        console.print(f"[yellow]No chunks found for {args.file}[/yellow]")

def handle_clear(args):
    """Handle clear command."""
    corpus = load_corpus(args.corpus)
    if corpus.clear():
        console.print("[green]✓[/green] Corpus cleared successfully")
    else:
        console.print("[yellow]Clear operation cancelled[/yellow]")

def handle_quick_ask(args):
    """Handle quick-ask command."""
    api_key = args.api_key or os.getenv(f"{args.provider.upper()}_API_KEY")
    
    if not api_key:
        console.print(f"[red]Error:[/red] API key required for {args.provider}")
        console.print(f"Set {args.provider.upper()}_API_KEY environment variable or use --api-key")
        return
    
    with Progress() as progress:
        task = progress.add_task("Processing document and generating answer...", total=None)
        
        answer = ask(
            file_path=args.file,
            query=args.query,
            api_key=api_key,
            provider=args.provider
        )
        
        progress.update(task, completed=True)
    
    console.print("\n")
    console.print(Panel.fit(
        Markdown(answer),
        title="[bold blue]Answer[/bold blue]",
        border_style="blue"
    ))

def load_corpus(corpus_name: str) -> DocCorpus:
    """Load a corpus by name or path."""
    # Check if it's a path
    corpus_path = Path(corpus_name)
    if corpus_path.exists():
        # Try to load from this path
        try:
            return DocCorpus(corpus_path=corpus_path)
        except:
            pass
    
    # Check default locations
    default_paths = [
        corpus_path,
        Path("./.docnav") / corpus_name,
        Path.home() / ".docnav" / corpus_name
    ]
    
    for path in default_paths:
        if (path / "corpus_index.pkl").exists():
            return DocCorpus(corpus_path=path)
    
    raise FileNotFoundError(f"Corpus '{corpus_name}' not found")

if __name__ == "__main__":
    main()
import typer
from typing import Optional
from pathlib import Path
from rich.console import Console
from rich.panel import Panel

app = typer.Typer(help="Advanced Financial Report Analyst CLI")
console = Console()

@app.command()
def ingest(
    file_path: str = typer.Argument(..., help="Path to PDF, HTML, or TXT file"),
    doc_id: Optional[str] = typer.Option(None, help="Unique ID for the document (default: filename)")
):
    """
    Ingest a document into the local knowledge base (SQLite + FAISS).
    """
    from ingestion.parser import DocumentParser
    from storage.database import DatabaseManager
    from storage.vector import VectorStore
    import uuid

    if not doc_id:
        doc_id = Path(file_path).stem

    console.print(f"[bold blue]Ingesting[/bold blue] {file_path} as ID: [cyan]{doc_id}[/cyan]...")
    
    try:
        # 1. Parse
        parser = DocumentParser()
        chunks = parser.parse_file(file_path)
        console.print(f"Parsed {len(chunks)} chunks/pages.")
        
        # 2. Store Metadata (DuckDB)
        db = DatabaseManager()
        db.add_document(doc_id, file_path)
        
        texts_to_embed = []
        metadatas_to_embed = []
        
        for chunk in chunks:
            chunk_id = str(uuid.uuid4())
            db.add_chunk(chunk_id, doc_id, chunk['content'], chunk['page'])
            
            texts_to_embed.append(chunk['content'])
            metadatas_to_embed.append({
                "doc_id": doc_id,
                "chunk_id": chunk_id,
                "content": chunk['content'],
                "page": chunk['page']
            })
            
        db.close()
        
        # 3. Embed & Vectorize (FAISS)
        console.print("Generating embeddings (this may take a moment)...")
        vector_store = VectorStore()
        vector_store.add_texts(texts_to_embed, metadatas_to_embed)
        
        console.print(f"[green]✓ Ingestion complete for {doc_id}[/green]")
        
    except Exception as e:
        console.print(f"[bold red]Error:[/bold red] {e}")

@app.command()
def analyze(
    doc_id: str = typer.Argument(..., help="Document ID to analyze"),
    report_type: str = typer.Option("summary", "--type", "-t", help="Type of report: summary, metrics, full")
):
    """
    Generate a financial analysis report for a stored document.
    """
    from agent.orchestrator import AgentOrchestrator
    import json
    
    console.print(f"[bold blue]Analyzing[/bold blue] {doc_id} for [cyan]{report_type}[/cyan]...")
    
    agent = AgentOrchestrator()
    report = agent.generate_report(doc_id, report_type)
    
    if "error" in report:
        console.print(f"[bold red]Error:[/bold red] {report['error']}")
        return

    # Render Report
    console.print(Panel(f"Report for {doc_id}", title=report_type.upper(), style="bold white"))
    
    console.print("\n[bold]Key Metrics:[/bold]")
    console.print(json.dumps(report["metrics"], indent=2))
    
    console.print("\n[bold]Executive Summary (Heuristic):[/bold]")
    console.print(report["summary"])
    
    console.print("\n[bold]Risks & Drivers (Extracted):[/bold]")
    for item in report["risks_and_drivers"]:
        console.print(f"- {item}")

@app.command()
def ask(
    query: str = typer.Argument(..., help="Natural language question"),
    doc_id: Optional[str] = typer.Option(None, help="Filter by specific document ID")
):
    """
    Ask a question about your financial documents (RAG).
    """
    from agent.orchestrator import AgentOrchestrator
    
    agent = AgentOrchestrator()
    result = agent.ask_question(query, doc_id)
    
    console.print(f"[bold yellow]Question:[/bold yellow] {query}")
    console.print(f"[bold green]Top Context Matches:[/bold green]")
    
    for i, cit in enumerate(result["citations"]):
        console.print(Panel(
            f"{cit['text']}\n[italic]Page: {cit['page']} | Score: {cit['score']:.4f}[/italic]",
            title=f"Citation {i+1}",
            border_style="cyan"
        ))

if __name__ == "__main__":
    app()

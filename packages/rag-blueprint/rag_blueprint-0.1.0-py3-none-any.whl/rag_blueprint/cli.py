import typer
from rich.console import Console
from pathlib import Path
from .generator import generate_project

app = typer.Typer(help="RAG Blueprint - Scaffolding for LLM RAG Projects")
console = Console()

@app.command()
def list():
    """List available RAG templates."""
    templates = ["simple", "advanced", "agentic"]
    console.print("[bold green]Available Templates:[/bold green]")
    for t in templates:
        console.print(f" - {t}")

@app.command()
def create(
    project_name: str = typer.Argument(..., help="Name of the project directory"),
    template: str = typer.Option(None, help="Template to use: simple, advanced, agentic")
):
    """Create a new RAG project from a template."""
    if template is None:
        # Interactive selection
        from rich.prompt import Prompt
        console.print("[bold]Select a template:[/bold]")
        console.print(" 1. [cyan]simple[/cyan]   - Basic RAG (LangChain + Chroma)")
        console.print(" 2. [cyan]advanced[/cyan] - Hybrid Search + Reranking")
        console.print(" 3. [cyan]agentic[/cyan]  - Agent with Tools (LangGraph)")
        
        choice = Prompt.ask("Choose", choices=["simple", "advanced", "agentic", "1", "2", "3"], default="simple")
        
        mapping = {"1": "simple", "2": "advanced", "3": "agentic"}
        template = mapping.get(choice, choice)

    console.print(f"[bold blue]Creating project '{project_name}' using template '{template}'...[/bold blue]")
    try:
        generate_project(project_name, template, Path.cwd())
        console.print(f"[bold green]Successfully created {project_name}![/bold green]")
    except Exception as e:
        console.print(f"[bold red]Error:[/bold red] {e}")

if __name__ == "__main__":
    app()

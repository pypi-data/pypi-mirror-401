import os

import httpx
import typer
from dotenv import load_dotenv
from rich.console import Console
from rich.table import Table

load_dotenv()

app = typer.Typer(help="Epist.ai Command Line Interface")
console = Console()

API_URL = os.getenv("EPIST_API_URL", "https://epist-api-prod-920152096400.us-central1.run.app/api/v1")
API_KEY = os.getenv("EPIST_API_KEY")


def get_client():
    if not API_KEY:
        console.print("[red]Error: EPIST_API_KEY environment variable is not set.[/red]")
        raise typer.Exit(code=1)
    return httpx.Client(base_url=API_URL, headers={"X-API-Key": API_KEY})


@app.command()
def login(key: str):
    """
    Configure your API Key (saves to .env file in current directory).
    """
    with open(".env", "a") as f:
        f.write(f"\nEPIST_API_KEY={key}\n")
    console.print("[green]API Key saved to .env[/green]")


@app.command()
def ingest(url: str, language: str = "en"):
    """
    Ingest audio from a URL.
    """
    with get_client() as client:
        try:
            response = client.post(
                "/audio/transcribe_url", json={"audio_url": url, "language": language, "rag_enabled": True}
            )
            response.raise_for_status()
            data = response.json()
            console.print(f"[green]Ingestion started![/green] ID: [bold]{data['id']}[/bold]")
        except httpx.HTTPError as e:
            console.print(f"[red]Error:[/red] {e}")


@app.command()
def status(audio_id: str):
    """
    Check the status of an audio task.
    """
    with get_client() as client:
        try:
            response = client.get(f"/audio/{audio_id}")
            response.raise_for_status()
            data = response.json()

            table = Table(title=f"Audio Status: {audio_id}")
            table.add_column("Property", style="cyan")
            table.add_column("Value", style="magenta")

            table.add_row("Status", data.get("status"))
            table.add_row("Title", data.get("title", "N/A"))

            console.print(table)
        except httpx.HTTPError as e:
            console.print(f"[red]Error:[/red] {e}")


@app.command()
def search(query: str, limit: int = 5):
    """
    Search the knowledge base.
    """
    with get_client() as client:
        try:
            response = client.post("/search/", json={"query": query, "limit": limit})
            response.raise_for_status()
            results = response.json()

            if not results:
                console.print("[yellow]No results found.[/yellow]")
                return

            for idx, r in enumerate(results, 1):
                score = f"{r['score'] * 100:.0f}%"
                console.print(f"[bold]{idx}. [{score}] ({r['start']:.0f}s - {r['end']:.0f}s)[/bold]")
                console.print(f"   {r['text']}")
                console.print("")

        except httpx.HTTPError as e:
            console.print(f"[red]Error:[/red] {e}")


if __name__ == "__main__":
    app()

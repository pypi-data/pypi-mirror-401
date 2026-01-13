"""
Command Line Interface for Assembly API Client.
"""

import asyncio
import logging
from typing import Optional

import typer
from rich.console import Console
from rich.table import Table

from .parser import SpecParser
from .sync import load_service_map, sync_all_services

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(message)s")
logger = logging.getLogger("assembly_client")

app = typer.Typer(help="Assembly API Client CLI")
console = Console()


def get_parser() -> SpecParser:
    """Get a configured SpecParser."""
    return SpecParser()


@app.command()
def sync(
    api_key: str = typer.Option(..., envvar="ASSEMBLY_API_KEY", help="API Key"),
    limit: Optional[int] = typer.Option(None, help="Limit number of services to sync"),
    force: bool = typer.Option(False, help="Force update master list"),
):
    """
    Synchronize API specifications.
    Downloads the master list and individual service specs.
    """
    parser = get_parser()
    console.print(f"[bold green]Starting sync...[/bold green] (Cache: {parser.cache_dir})")

    async def run_sync():
        stats = await sync_all_services(api_key=api_key, parser=parser, limit=limit, force_update_list=force)
        return stats

    stats = asyncio.run(run_sync())

    console.print("\n[bold]Sync Complete[/bold]")
    console.print(f"Updated: [green]{stats['updated']}[/green]")
    console.print(f"Failed: [red]{stats['failed']}[/red]")


@app.command("list")
def list_apis(
    search: Optional[str] = typer.Option(None, help="Filter by name or ID"),
):
    """
    List available APIs from the cached master list.
    """
    parser = get_parser()
    service_map = load_service_map(parser.cache_dir)

    if not service_map:
        console.print("[yellow]No APIs found. Run 'sync' first.[/yellow]")
        return

    table = Table(title="Available APIs")
    table.add_column("Service ID", style="cyan")
    table.add_column("Name", style="green")

    count = 0
    for sid, name in sorted(service_map.items()):
        if search and (search.lower() not in sid.lower() and search.lower() not in name.lower()):
            continue
        table.add_row(sid, name)
        count += 1

    console.print(table)
    console.print(f"Total: {count} APIs")


@app.command()
def info(service_id: str):
    """
    Show details for a specific API service.
    """
    parser = get_parser()

    async def get_spec():
        return await parser.parse_spec(service_id)

    try:
        spec = asyncio.run(get_spec())

        console.print(f"[bold]Service ID:[/bold] {spec.service_id}")
        console.print(f"[bold]Endpoint:[/bold] {spec.endpoint}")
        console.print(f"[bold]URL:[/bold] {spec.endpoint_url}")

        table = Table(title="Request Parameters")
        table.add_column("Name", style="cyan")
        table.add_column("Type", style="magenta")
        table.add_column("Required", style="red")
        table.add_column("Description")

        for p in spec.request_params:
            table.add_row(p.name, p.type, "Yes" if p.required else "No", p.description)

        console.print(table)

    except Exception as e:
        console.print(f"[red]Error fetching spec for {service_id}: {e}[/red]")


if __name__ == "__main__":
    app()

"""Main CLI application"""
import typer
from typing import Optional
from rich.console import Console
from rich.table import Table
from rich import print as rprint
import pyperclip
from spark.database import (
    save_snippet,
    find_snippets,
    get_all_snippets,
    get_snippet_by_id,
    delete_snippet,
    find_snippets_by_text,
    delete_snippets_by_text,
    clear_all_snippets,
    command_exists,
)
from spark.autotag import generate_auto_tags, merge_tags

app = typer.Typer(
    name="spark",
    help="Your intelligent code snippet manager",
    add_completion=False,
    no_args_is_help=True,
)

console = Console(force_terminal=True, legacy_windows=False)


@app.command()
def save(
    command: str = typer.Argument(..., help="Command to save"),
    tags: Optional[str] = typer.Option(None, "--tags", "-t", help="Comma-separated tags"),
    no_auto_tags: bool = typer.Option(False, "--no-auto-tags", help="Disable automatic tagging"),
):
    """Save a new code snippet with intelligent auto-tagging"""
    existing = command_exists(command)
    
    if existing:
        rprint(f"[yellow]This command already exists as snippet #{existing['id']}[/yellow]")
        rprint(f"[dim]{command}[/dim]")
        if not typer.confirm("Do you want to add it anyway?"):
            rprint("[dim]Cancelled[/dim]")
            raise typer.Exit(0)
    
    # Generate auto-tags if enabled
    final_tags = tags
    auto_tags = None
    
    if not no_auto_tags:
        auto_tags = generate_auto_tags(command, include_context=True)
        if auto_tags:
            final_tags = merge_tags(manual_tags=tags, auto_tags=auto_tags)
            if tags:
                rprint(f"[cyan]Auto-tags:[/cyan] [magenta]{auto_tags}[/magenta] [dim](merged with your tags)[/dim]")
            else:
                rprint(f"[cyan]Auto-tags:[/cyan] [magenta]{auto_tags}[/magenta]")
    
    snippet_id = save_snippet(command, final_tags)
    rprint(f"[green]Saved snippet #{snippet_id}[/green]")
    rprint(f"[dim]{command}[/dim]")
    if final_tags:
        rprint(f"[dim]Tags: {final_tags}[/dim]")


@app.command()
def find(
    search_term: str = typer.Argument(..., help="Search term"),
):
    """Find snippets by search term"""
    results = find_snippets(search_term)
    
    if not results:
        rprint(f"[yellow]No snippets found for '{search_term}'[/yellow]")
        return
    
    table = Table(title=f"Found {len(results)} snippet(s)")
    table.add_column("ID", style="cyan", width=6)
    table.add_column("Command", style="white")
    table.add_column("Tags", style="magenta", width=20)
    table.add_column("Created", style="dim")
    
    for snippet in results:
        tags = snippet.get("tags", "") or ""
        table.add_row(
            str(snippet["id"]),
            snippet["command"],
            tags,
            snippet["created_at"][:10] if snippet["created_at"] else "",
        )
    
    console.print(table)


@app.command()
def list(
    tag: Optional[str] = typer.Option(None, "--tag", help="Filter by tag"),
):
    """List all snippets"""
    results = get_all_snippets(tag_filter=tag)
    
    if not results:
        if tag:
            rprint(f"[yellow]No snippets found with tag '{tag}'[/yellow]")
        else:
            rprint("[yellow]No snippets saved yet[/yellow]")
        return
    
    title = f"All snippets ({len(results)})"
    if tag:
        title = f"Snippets with tag '{tag}' ({len(results)})"
    
    table = Table(title=title)
    table.add_column("ID", style="cyan", width=6)
    table.add_column("Command", style="white")
    table.add_column("Tags", style="magenta", width=20)
    table.add_column("Created", style="dim")
    
    for snippet in results:
        tags = snippet.get("tags", "") or ""
        table.add_row(
            str(snippet["id"]),
            snippet["command"],
            tags,
            snippet["created_at"][:10] if snippet["created_at"] else "",
        )
    
    console.print(table)


@app.command()
def copy(
    snippet_id: int = typer.Argument(..., help="Snippet ID to copy"),
):
    """Copy snippet to clipboard"""
    snippet = get_snippet_by_id(snippet_id)
    
    if not snippet:
        rprint(f"[red]Snippet #{snippet_id} not found[/red]")
        raise typer.Exit(1)
    
    pyperclip.copy(snippet["command"])
    rprint(f"[blue]Copied snippet #{snippet_id} to clipboard[/blue]")
    rprint(f"[dim]{snippet['command']}[/dim]")


@app.command()
def delete(
    identifier: str = typer.Argument(..., help="Snippet ID or text to delete"),
):
    """Delete a snippet by ID or by text content"""
    # Try to parse as integer (ID)
    try:
        snippet_id = int(identifier)
        # Delete by ID
        snippet = get_snippet_by_id(snippet_id)
        
        if not snippet:
            rprint(f"[red]Snippet #{snippet_id} not found[/red]")
            raise typer.Exit(1)
        
        deleted = delete_snippet(snippet_id)
        if deleted:
            rprint(f"[green]Deleted snippet #{snippet_id}[/green]")
            rprint(f"[dim]{snippet['command']}[/dim]")
    except ValueError:
        # Not a number, treat as search text
        matching = find_snippets_by_text(identifier)
        
        if not matching:
            rprint(f"[yellow]No snippets found containing '{identifier}'[/yellow]")
            return
        
        # Show what will be deleted
        rprint(f"[yellow]Found {len(matching)} snippet(s) containing '{identifier}':[/yellow]")
        table = Table()
        table.add_column("ID", style="cyan", width=6)
        table.add_column("Command", style="white")
        table.add_column("Tags", style="magenta", width=20)
        table.add_column("Created", style="dim")
        
        for snippet in matching:
            tags = snippet.get("tags", "") or ""
            table.add_row(
                str(snippet["id"]),
                snippet["command"],
                tags,
                snippet["created_at"][:10] if snippet["created_at"] else "",
            )
        
        console.print(table)
        
        if typer.confirm(f"Delete all {len(matching)} snippet(s)?"):
            deleted_count = delete_snippets_by_text(identifier)
            rprint(f"[green]Deleted {deleted_count} snippet(s)[/green]")
        else:
            rprint("[dim]Cancelled[/dim]")
            raise typer.Exit(0)


@app.command()
def clear():
    """Delete all snippets"""
    count = clear_all_snippets()
    rprint(f"[green]Deleted {count} snippet(s)[/green]")


if __name__ == "__main__":
    app()


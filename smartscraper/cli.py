"""Command-line interface for SmartScraper."""

import sys
import json
from typing import Optional

import click
from rich.console import Console
from rich.table import Table
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.panel import Panel
from rich.syntax import Syntax

from .core.scraper import SmartScraper


console = Console()


@click.group(invoke_without_command=True)
@click.option("--url", "-u", help="Target URL to scrape")
@click.option("--describe", "-d", default="", help="Natural language description of what to extract")
@click.option("--selector", "-s", default=None, help="CSS selector for extraction")
@click.option("--output", "-o", default=None, help="Output file path")
@click.option("--format", "-f", "fmt", default="auto", type=click.Choice(["auto", "json", "csv", "md", "txt"]))
@click.option("--timeout", "-t", default=30, help="Request timeout in seconds")
@click.option("--retries", "-r", default=3, help="Number of retries")
@click.option("--delay", default=1.0, help="Delay between requests")
@click.option("--verbose", "-v", is_flag=True, help="Verbose output")
@click.pass_context
def main(ctx, url, describe, selector, output, fmt, timeout, retries, delay, verbose):
    """SmartScraper - Zero-config intelligent web scraping framework.
    
    Examples:
        ss -u https://example.com
        ss -u https://example.com -d "extract all links"
        ss -u https://example.com -s "h1" -o titles.json
    """
    if ctx.invoked_subcommand is not None:
        return
    
    if not url:
        console.print(Panel(
            "[bold cyan]SmartScraper[/bold cyan] - Zero-config intelligent web scraping\n\n"
            "Usage: ss -u <URL> [OPTIONS]\n\n"
            "Examples:\n"
            "  ss -u https://example.com\n"
            "  ss -u https://example.com -d \"extract all links\"\n"
            "  ss -u https://example.com -s \"article h2\" -o articles.json",
            title="SmartScraper CLI",
            border_style="green"
        ))
        return

    scraper = SmartScraper(timeout=timeout, retries=retries, delay=delay)
    
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console,
        transient=True,
    ) as progress:
        task = progress.add_task(f"[cyan]Scraping {url}...", total=None)
        try:
            result = scraper.scrape(url, description=describe, selector=selector)
            progress.update(task, description="[green]Done!")
        except Exception as e:
            progress.update(task, description=f"[red]Error: {e}")
            console.print(f"[bold red]Error:[/bold red] {e}")
            sys.exit(1)

    # Display results
    _display_results(result, verbose)
    
    # Save to file if specified
    if output:
        result.save(output, fmt)
        console.print(f"\n[green]Saved to {output}[/green]")


def _display_results(result, verbose: bool = False):
    """Display scraping results in a rich format."""
    console.print(f"\n[bold green]Title:[/bold green] {result.title or 'N/A'}")
    console.print(f"[bold green]URL:[/bold green] {result.url}")
    console.print(f"[bold green]Items:[/bold green] {len(result)}\n")
    
    if not result.data:
        console.print("[yellow]No data extracted.[/yellow]")
        return

    # Show first few items
    display_count = min(5, len(result.data))
    for i, item in enumerate(result.data[:display_count], 1):
        if isinstance(item, dict):
            # Create a table for each item
            table = Table(show_header=False, box=None, padding=(0, 2))
            table.add_column("Key", style="cyan", no_wrap=True)
            table.add_column("Value", style="white")
            for k, v in item.items():
                v_str = str(v)
                if len(v_str) > 200 and not verbose:
                    v_str = v_str[:200] + "..."
                table.add_row(str(k), v_str)
            console.print(Panel(table, title=f"Item {i}", border_style="blue"))
        else:
            console.print(f"[{i}] {item}")
    
    if len(result.data) > display_count:
        console.print(f"[dim]... and {len(result.data) - display_count} more items[/dim]")
    
    # Show JSON preview
    if verbose:
        console.print("\n[bold]JSON Preview:[/bold]")
        json_str = result.to_json(indent=2)
        if len(json_str) > 2000:
            json_str = json_str[:2000] + "\n..."
        syntax = Syntax(json_str, "json", theme="monokai", line_numbers=False)
        console.print(syntax)


@main.command()
@click.argument("urls", nargs=-1, required=True)
@click.option("--describe", "-d", default="", help="Description of what to extract")
@click.option("--output", "-o", required=True, help="Output directory")
@click.option("--format", "-f", "fmt", default="json", type=click.Choice(["json", "csv", "md", "txt"]))
def batch(urls, describe, output, fmt):
    """Scrape multiple URLs in batch mode."""
    import os
    os.makedirs(output, exist_ok=True)
    
    scraper = SmartScraper()
    results = scraper.scrape_batch(list(urls), description=describe)
    
    for url, result in results.items():
        safe_name = "".join(c if c.isalnum() else "_" for c in url.split("://")[-1])
        filepath = os.path.join(output, f"{safe_name}.{fmt}")
        result.save(filepath, fmt)
        status = "[green]OK[/green]" if not any("error" in str(d) for d in result.data) else "[red]ERR[/red]"
        console.print(f"{status} {url} -> {filepath}")


@main.command()
@click.argument("url")
@click.option("--pattern", "-p", default=None, help="Regex pattern to filter links")
@click.option("--max", "-m", default=20, help="Maximum links to show")
def links(url, pattern, max):
    """Extract all links from a page."""
    scraper = SmartScraper()
    link_list = scraper.scrape_links(url, pattern=pattern, max_links=max)
    
    table = Table(title=f"Links from {url}")
    table.add_column("#", style="cyan", no_wrap=True)
    table.add_column("Text", style="green")
    table.add_column("URL", style="blue")
    
    for i, link in enumerate(link_list, 1):
        text = link.get("text", "")[:40]
        href = link.get("href", "")[:60]
        table.add_row(str(i), text, href)
    
    console.print(table)
    console.print(f"\nTotal: {len(link_list)} links")


@main.command()
def version():
    """Show version information."""
    from . import __version__
    console.print(f"[bold cyan]SmartScraper[/bold cyan] version [bold]{__version__}[/bold]")


if __name__ == "__main__":
    main()

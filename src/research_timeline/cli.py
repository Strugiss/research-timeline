"""Research Timeline - CLI tool for tracking research progress."""

import json
import yaml
from datetime import datetime
from pathlib import Path
from typing import Optional

import click
from rich.console import Console
from rich.table import Table

console = Console()

DEFAULT_FILE = Path("research_timeline.yaml")


def load_timeline(path: Path) -> dict:
    if path.exists():
        with open(path, "r", encoding="utf-8") as f:
            return yaml.safe_load(f) or {"entries": []}
    return {"entries": []}


def save_timeline(path: Path, data: dict) -> None:
    with open(path, "w", encoding="utf-8") as f:
        yaml.dump(data, f, allow_unicode=True, sort_keys=False)


def validate_timeline(data: dict) -> list:
    errors = []
    for i, entry in enumerate(data.get("entries", [])):
        if "date" not in entry:
            errors.append(f"Entry {i}: missing 'date'")
        if "title" not in entry:
            errors.append(f"Entry {i}: missing 'title'")
        if "status" not in entry:
            errors.append(f"Entry {i}: missing 'status'")
        if entry.get("status") not in ["pending", "in_progress", "completed", "cancelled"]:
            errors.append(f"Entry {i}: invalid status '{entry.get('status')}'")
    return errors


@click.group()
@click.version_option(version="0.1.0")
def main():
    """Research Timeline - Track your research progress."""
    pass


@main.command()
@click.option("--file", "-f", default=str(DEFAULT_FILE), help="Timeline file path")
def init(file: str):
    """Initialize a new timeline file."""
    path = Path(file)
    if path.exists():
        console.print(f"[yellow]Timeline already exists at {path}[/yellow]")
        return
    data = {"entries": [], "created": datetime.now().isoformat()}
    save_timeline(path, data)
    console.print(f"[green]Created timeline at {path}[/green]")


@main.command()
@click.option("--file", "-f", default=str(DEFAULT_FILE), help="Timeline file path")
@click.argument("title")
@click.option("--status", "-s", default="pending", type=click.Choice(["pending", "in_progress", "completed", "cancelled"]))
@click.option("--date", "-d", default=None, help="Date (ISO format), defaults to today")
@click.option("--tags", "-t", default="", help="Comma-separated tags")
@click.option("--notes", "-n", default="", help="Additional notes")
def log(file: str, title: str, status: str, date: Optional[str], tags: str, notes: str):
    """Add a new entry to the timeline."""
    path = Path(file)
    data = load_timeline(path)
    entry = {
        "date": date or datetime.now().date().isoformat(),
        "title": title,
        "status": status,
        "tags": [t.strip() for t in tags.split(",") if t.strip()],
        "notes": notes,
    }
    data["entries"].append(entry)
    save_timeline(path, data)
    console.print(f"[green]Logged: {title} ({status})[/green]")


@main.command()
@click.option("--file", "-f", default=str(DEFAULT_FILE), help="Timeline file path")
@click.option("--status", "-s", help="Filter by status")
@click.option("--tag", "-t", help="Filter by tag")
@click.option("--limit", "-l", default=0, help="Limit number of entries (0 = all)")
def list(file: str, status: Optional[str], tag: Optional[str], limit: int):
    """List timeline entries."""
    path = Path(file)
    data = load_timeline(path)
    entries = data.get("entries", [])

    if status:
        entries = [e for e in entries if e.get("status") == status]
    if tag:
        entries = [e for e in entries if tag in e.get("tags", [])]

    entries = sorted(entries, key=lambda e: e.get("date", ""), reverse=True)
    if limit > 0:
        entries = entries[:limit]

    table = Table(title="Research Timeline")
    table.add_column("Date", style="cyan")
    table.add_column("Title", style="bold")
    table.add_column("Status", style="green")
    table.add_column("Tags", style="yellow")
    table.add_column("Notes", style="dim")

    for e in entries:
        table.add_row(
            e.get("date", ""),
            e.get("title", ""),
            e.get("status", ""),
            ", ".join(e.get("tags", [])),
            e.get("notes", "")[:50] + ("..." if len(e.get("notes", "")) > 50 else ""),
        )
    console.print(table)


@main.command()
@click.option("--file", "-f", default=str(DEFAULT_FILE), help="Timeline file path")
@click.option("--format", "-F", "fmt", default="yaml", type=click.Choice(["yaml", "json", "md"]))
@click.option("--output", "-o", default=None, help="Output file (stdout if not specified)")
def export(file: str, fmt: str, output: Optional[str]):
    """Export timeline to various formats."""
    path = Path(file)
    data = load_timeline(path)
    entries = data.get("entries", [])

    if fmt == "yaml":
        content = yaml.dump({"entries": entries}, allow_unicode=True, sort_keys=False)
    elif fmt == "json":
        content = json.dumps({"entries": entries}, indent=2, ensure_ascii=False)
    else:  # markdown
        lines = ["# Research Timeline", ""]
        for e in sorted(entries, key=lambda x: x.get("date", "")):
            status_icon = {"pending": "⏳", "in_progress": "🔄", "completed": "✅", "cancelled": "❌"}.get(e.get("status"), "❓")
            lines.append(f"## {status_icon} {e.get('title')} ({e.get('date')})")
            if e.get("tags"):
                lines.append(f"**Tags:** {', '.join(e['tags'])}")
            if e.get("notes"):
                lines.append(f"**Notes:** {e['notes']}")
            lines.append("")
        content = "\n".join(lines)

    if output:
        Path(output).write_text(content, encoding="utf-8")
        console.print(f"[green]Exported to {output}[/green]")
    else:
        console.print(content)


@main.command()
@click.option("--file", "-f", default=str(DEFAULT_FILE), help="Timeline file path")
def validate(file: str):
    """Validate timeline for errors."""
    path = Path(file)
    data = load_timeline(path)
    errors = validate_timeline(data)

    if errors:
        console.print("[red]Validation errors:[/red]")
        for err in errors:
            console.print(f"  - {err}")
        raise SystemExit(1)
    else:
        console.print(f"[green]Timeline valid ({len(data.get('entries', []))} entries)[/green]")


if __name__ == "__main__":
    main()
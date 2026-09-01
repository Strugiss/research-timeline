import typer
from typing import Optional, List
from datetime import date
from pathlib import Path
import json
import re
from rich.console import Console
from rich.table import Table
from rich import print as rprint

from .models import ResearchTimeline, ProjectInfo, Author, Event

VALID_EVENT_ID = re.compile(r"^T([0-9]+|n)$|^(pivot|control|submission|publication|milestone)$")

app = typer.Typer(
    name="research-timeline",
    help="Track, visualize, and export research timelines from first AI interaction to scientific discovery",
    add_completion=False,
    no_args_is_help=True,
)

console = Console()

# Default timeline file
DEFAULT_TIMELINE_FILE = Path(".research-timeline.json")


def load_timeline(path: Path) -> Optional[dict]:
    """Load timeline from JSON file."""
    if not path.exists():
        return None
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)


def save_timeline(path: Path, data: dict) -> None:
    """Save timeline to JSON file."""
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def print_ok(msg: str) -> None:
    """Print success message."""
    print(f"[OK] {msg}")


def print_error(msg: str) -> None:
    print(f"[ERROR] {msg}")


@app.command()
def init(
    name: str = typer.Option(..., "--name", "-n", help="Project name"),
    description: str = typer.Option(..., "--desc", "-d", help="Project description"),
    domain: str = typer.Option("quantum", "--domain", help="Research domain"),
    author_name: str = typer.Option(..., "--author", "-a", help="Author name"),
    affiliation: str = typer.Option("independent", "--affiliation", help="Affiliation"),
    orcid: Optional[str] = typer.Option(None, "--orcid", help="ORCID URL"),
    background: str = typer.Option("without academic degrees", "--background", help="Academic background"),
    ai_role: str = typer.Option("cognitive_prosthesis", "--ai-role", help="AI role"),
    output: Path = typer.Option(Path(".research-timeline.json"), "--output", "-o", help="Output file"),
):
    """Initialize a new research timeline."""
    from datetime import date
    
    timeline = {
        "project": {
            "name": name,
            "description": description,
            "domain": domain
        },
        "author": {
            "name": author_name,
            "affiliation": affiliation,
            "orcid": orcid,
            "background": background,
            "ai_role": ai_role
        },
        "events": [],
        "created_at": str(date.today()),
        "updated_at": str(date.today()),
        "version": "1.0"
    }
    
    output_path = Path(output)
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(timeline, f, indent=2, ensure_ascii=False)
    
    print(f"[OK] Initialized timeline at {output}")
    print(f"  Project: {name} ({domain})")
    print(f"  Author: {author_name} ({background})")


@app.command()
def log(
    event_id: str = typer.Argument(..., help="Event ID (T0, T1, T2, Tn, pivot, control, etc.)"),
    event_type: str = typer.Option(..., "--type", help="Event type (T0, T1, T2, Tn, pivot, control, submission, publication, milestone)"),
    event_date: str = typer.Option(str(date.today()), "--date", help="Event date (YYYY-MM-DD)"),
    end_date: Optional[str] = typer.Option(None, "--end-date", help="Optional end date for a range (YYYY-MM-DD)"),
    description: str = typer.Option(..., "--desc", help="Event description"),
    tags: Optional[str] = typer.Option(None, "--tags", help="Tags (comma-separated)"),
    z_score: Optional[float] = typer.Option(None, "--z-score", help="Z-score"),
    shots: Optional[int] = typer.Option(None, "--shots", help="Number of shots"),
    backend: Optional[str] = typer.Option(None, "--backend", help="Quantum backend"),
    job_ids: Optional[List[str]] = typer.Option(None, "--job-ids", help="Job IDs (comma-separated)"),
    z_score_combined: Optional[float] = typer.Option(None, "--z-combined", help="Combined Z-score"),
    git_commit: Optional[str] = typer.Option(None, "--git-commit", help="Git commit hash"),
    data_links: Optional[List[str]] = typer.Option(None, "--data-links", help="Data links (comma-separated)"),
    code_links: Optional[List[str]] = typer.Option(None, "--code-links", help="Code links (comma-separated)"),
    timeline_file: Path = typer.Option(Path(".research-timeline.json"), "--file", "-f", help="Timeline file"),
):
    """Log a new event to the timeline."""
    if not Path(timeline_file).exists():
        print(f"[ERROR] Timeline file not found: {timeline_file}. Run 'init' first.")
        raise typer.Exit(1)
    
    with open(timeline_file, 'r', encoding='utf-8') as f:
        timeline = json.load(f)
    
    # Validate event ID
    event_id = event_id.strip()
    if not VALID_EVENT_ID.match(event_id):
        print("[ERROR] Event ID must match T0, T1, T2, Tn, pivot, control, submission, publication, milestone")
        raise typer.Exit(1)
    
    # Check for duplicate ID
    for event in timeline.get("events", []):
        if event.get("id") == event_id:
            print(f"[ERROR] Event ID {event_id} already exists")
            raise typer.Exit(1)
    
    # Build event
    event = {
        "id": event_id,
        "type": event_type,
        "date": event_date,
        "description": description,
        "tags": [t.strip() for t in tags.split(",")] if tags else [],
    }
    if end_date:
        event["end_date"] = end_date
    
    # Add metrics if provided
    metrics = {}
    if z_score is not None:
        metrics["z_score"] = z_score
    if shots is not None:
        metrics["shots"] = shots
    if backend:
        metrics["backend"] = backend
    if z_score_combined is not None:
        metrics["z_score_combined"] = z_score_combined
    if metrics:
        event["metrics"] = {k: v for k, v in metrics.items() if v is not None}
    
    # Evidence
    evidence = {}
    if git_commit:
        evidence["git_commit"] = git_commit
    if job_ids:
        evidence["job_ids"] = [j.strip() for tok in job_ids for j in tok.split(",") if j.strip()]
    if data_links:
        evidence["data_links"] = [d.strip() for tok in data_links for d in tok.split(",") if d.strip()]
    if code_links:
        evidence["code_links"] = [c.strip() for tok in code_links for c in tok.split(",") if c.strip()]
    if evidence:
        event["evidence"] = {k: v for k, v in evidence.items() if v}
    
    timeline.setdefault("events", []).append(event)
    timeline["updated_at"] = str(date.today())
    
    with open(timeline_file, 'w', encoding='utf-8') as f:
        json.dump(timeline, f, indent=2, ensure_ascii=False)
    
    print(f"[OK] Logged event {event_id}: {description}")


@app.command()
def list(
    timeline_file: Path = typer.Option(Path(".research-timeline.json"), "--file", "-f", help="Timeline file"),
    show_metrics: bool = typer.Option(False, "--metrics", "-m", help="Show metrics"),
    event_type: Optional[str] = typer.Option(None, "--type", help="Filter by event type"),
    tag: Optional[str] = typer.Option(None, "--tag", help="Filter by tag (exact match)"),
    since: Optional[str] = typer.Option(None, "--since", help="Only events with date >= YYYY-MM-DD"),
    until: Optional[str] = typer.Option(None, "--until", help="Only events with date <= YYYY-MM-DD"),
):
    """List all events in the timeline (with optional filters)."""
    if not Path(timeline_file).exists():
        print(f"[ERROR] Timeline file not found: {timeline_file}")
        raise typer.Exit(1)

    with open(timeline_file, 'r', encoding='utf-8') as f:
        timeline = json.load(f)

    events = timeline.get("events", [])

    if event_type:
        events = [e for e in events if e.get("type") == event_type]
    if tag:
        events = [e for e in events if tag in e.get("tags", [])]
    if since:
        events = [e for e in events if e.get("date", "") >= since]
    if until:
        events = [e for e in events if e.get("date", "") <= until]

    # Print as simple text table to avoid Unicode issues on Windows
    print("Research Timeline")
    print("=" * 80)
    header = f"{'ID':<4} | {'Type':<6} | {'Date':<12} | {'Description':<40} | {'Tags':<20} | {'Metrics':<30}"
    print(header)
    print("-" * 120)

    for event in events:
        metrics_str = ""
        if event.get("metrics"):
            # Replace sigma character for Windows compatibility
            metrics_str = ", ".join(f"{k}={v}".replace('\u03c3', 'sigma') for k, v in event.get("metrics", {}).items() if v is not None)

        desc = event["description"][:50]
        tags_str = ", ".join(event.get("tags", []))
        print(f"{event['id']:<4} | {event['type']:<6} | {event['date']:<12} | {desc:<50} | {tags_str:<20} | {metrics_str}")


@app.command()
def export(
    format: str = typer.Option("latex", "--format", help="Export format: latex, markdown, jsonld, html, csv, gantt"),
    timeline_file: Path = typer.Option(Path(".research-timeline.json"), "--file", help="Timeline file"),
    output: Optional[Path] = typer.Option(None, "--output", "-o", help="Output file"),
):
    """Export timeline to various formats."""
    if not Path(timeline_file).exists():
        print(f"[ERROR] Timeline file not found: {timeline_file}")
        raise typer.Exit(1)
    
    with open(timeline_file, 'r', encoding='utf-8') as f:
        timeline = json.load(f)
    
    if format == "latex":
        output_content = export_latex(timeline)
    elif format == "markdown":
        output_content = export_markdown(timeline)
    elif format == "jsonld":
        output_content = export_jsonld(timeline)
    elif format == "html":
        output_content = export_html(timeline)
    elif format == "csv":
        output_content = export_csv(timeline)
    elif format == "gantt":
        output_content = export_gantt(timeline)
    else:
        print(f"[ERROR] Unknown format: {format}")
        raise typer.Exit(1)
    
    if output:
        with open(output, 'w', encoding='utf-8') as f:
            f.write(output_content)
        print(f"[OK] Exported to {output}")
    else:
        print(output_content)


def export_csv(timeline: dict) -> str:
    """Export timeline as CSV (machine-readable, spreadsheet-friendly)."""
    import csv
    import io
    import builtins
    buf = io.StringIO()
    w = csv.writer(buf)
    w.writerow(["id", "type", "date", "description", "tags", "metrics", "evidence"])
    for event in timeline.get("events", []):
        metrics = event.get("metrics", {})
        metrics_str = "; ".join(f"{k}={v}" for k, v in metrics.items() if v is not None)
        evidence = event.get("evidence", {})
        ev_parts = []
        for k, v in evidence.items():
            if isinstance(v, builtins.list):
                ev_parts.append(f"{k}: {','.join(v)}")
            else:
                ev_parts.append(f"{k}: {v}")
        w.writerow([
            event["id"], event["type"], event["date"], event["description"],
            ";".join(event.get("tags", [])), metrics_str, " | ".join(ev_parts),
        ])
    return buf.getvalue()


def export_gantt(timeline: dict) -> str:
    """Export timeline as a publication-ready Gantt chart (LaTeX TikZ).

    Requires \\usepackage{tikz} in the document. Dates are positioned on a
    horizontal axis; event ranges (start/end) render as bars, point events as
    markers. Style follows the academic timeline convention.
    """
    from datetime import date

    events = timeline.get("events", [])
    if not events:
        return "% No events to render."
    dates = []
    for e in events:
        d0 = e.get("date", "")
        d1 = e.get("end_date") or d0
        dates.append((d0, d1))
    start = min(d[0] for d in dates)
    end = max(d[1] for d in dates)

    def days(a, b):
        try:
            return (date.fromisoformat(b) - date.fromisoformat(a)).days
        except ValueError:
            return 0

    total = max(days(start, end), 1)
    n = len(events)
    row_h = 0.9
    axis_h = 1.2

    lines = [
        "% Research Timeline -- Gantt (TikZ). Requires: \\\\usepackage{tikz}",
        "\\begin{tikzpicture}[x=6cm/%.1f,y=%.2fcm]" % (total, row_h),
        "  % time axis",
        f"  \\draw[->] (0,{axis_h}) -- (1.02,{axis_h});",
    ]
    # axis labels (start and end)
    lines.append(f"  \\node[below] at (0,{axis_h}) {{{start}}};")
    lines.append(f"  \\node[below] at (1,{axis_h}) {{{end}}};")

    for i, (e, (d0, d1)) in enumerate(zip(events, dates)):
        y = axis_h - (i + 1) * row_h
        x0 = days(start, d0) / total
        w = max(days(d0, d1) / total, 0.02)
        desc = e["description"][:40].replace("&", r"\&").replace("%", r"\%").replace("_", r"\_")
        # label on the left
        lines.append(f"  \\node[anchor=east,align=right] at (0,{y:.2f}) {{{e['id']} \\textsc{{{e['type']}}}}};")
        # bar or marker
        if d1 != d0:
            lines.append(f"  \\draw[fill=blue!25] ({x0:.3f},{y:.2f}) rectangle ({x0 + w:.3f},{y + 0.45:.2f});")
        else:
            lines.append(f"  \\draw[fill=black] ({x0:.3f},{y + 0.2:.2f}) circle (1.5pt);")
        # description under the row
        lines.append(f"  \\node[anchor=west,font=\\scriptsize] at (0,{y - 0.30:.2f}) {{{desc}}};")

    lines.append("\\end{tikzpicture}")
    return "\n".join(lines)


@app.command()
def stats(
    timeline_file: Path = typer.Option(Path(".research-timeline.json"), "--file", "-f", help="Timeline file"),
):
    """Print summary statistics of the timeline (duration, per-type counts, window)."""
    if not Path(timeline_file).exists():
        print(f"[ERROR] Timeline file not found: {timeline_file}")
        raise typer.Exit(1)

    with open(timeline_file, 'r', encoding='utf-8') as f:
        timeline = json.load(f)

    events = timeline.get("events", [])
    if not events:
        print("No events recorded.")
        raise typer.Exit(0)

    types = {}
    for e in events:
        t = e.get("type", "?")
        types[t] = types.get(t, 0) + 1

    dates = [e.get("date", "") for e in events if e.get("date")]
    d0 = min(dates)
    d1 = max(dates)

    from datetime import date
    try:
        days = (date.fromisoformat(d1) - date.fromisoformat(d0)).days
    except ValueError:
        days = 0

    print(f"Events:      {len(events)}")
    print(f"Date window: {d0} .. {d1} ({days} days)")
    print("By type:")
    for t, c in sorted(types.items()):
        print(f"  {t:<14} {c}")
    print("By tag:")
    tags = {}
    for e in events:
        for tg in e.get("tags", []):
            tags[tg] = tags.get(tg, 0) + 1
    for tg, c in sorted(tags.items()):
        print(f"  {tg:<14} {c}")


def export_latex(timeline: dict) -> str:
    """Export timeline as LaTeX table."""
    lines = [
        "\\begin{table}[ht]",
        "\\centering",
        "\\caption{Research Timeline: First AI Interaction to Discovery}",
        "\\label{tab:timeline}",
        "\\begin{tabular}{lllll}",
        "\\toprule",
        "\\textbf{Phase} & \\textbf{Date} & \\textbf{Event} & \\textbf{Metrics} & \\textbf{Evidence} \\\\",
        "\\midrule",
    ]
    
    for event in timeline.get("events", []):
        metrics = event.get("metrics", {})
        metrics_str = ", ".join(f"{k}={v}" for k, v in metrics.items() if v is not None) if metrics else ""
        evidence = event.get("evidence", {})
        evidence_str = ""
        if evidence.get("git_commit"):
            evidence_str += f"git {evidence['git_commit'][:8]} "
        if evidence.get("job_ids"):
            evidence_str += f"jobs: {', '.join(evidence['job_ids'][:3])} "
        
        lines.append(
            f"{event['id']} & {event['date']} & {event['description'][:50]} & {metrics_str} & {evidence_str} \\\\"
        )
    
    lines.extend([
        "\\bottomrule",
        "\\end{tabular}",
        "\\end{table}",
    ])
    return "\n".join(lines)


def export_markdown(timeline: dict) -> str:
    """Export timeline as Markdown table."""
    lines = ["## Research Timeline", "", "| Phase | Date | Event | Metrics | Evidence |", "|-------|------|-------|---------|----------|"]
    
    for event in timeline.get("events", []):
        metrics = event.get("metrics", {})
        metrics_str = ", ".join(f"{k}={v}" for k, v in metrics.items() if v is not None) if metrics else ""
        evidence = event.get("evidence", {})
        evidence_str = ""
        if evidence.get("git_commit"):
            evidence_str += f"git {evidence['git_commit'][:8]} "
        if evidence.get("job_ids"):
            evidence_str += f"jobs: {', '.join(evidence['job_ids'][:3])} "
        
        lines.append(f"| {event['id']} | {event['date']} | {event['description'][:60]} | {metrics_str} | {evidence_str} |")
    
    return "\n".join(lines)


def export_jsonld(timeline: dict) -> str:
    """Export as JSON-LD for Schema.org."""
    context = {
        "@context": "https://schema.org",
        "@type": "ResearchProject",
        "name": timeline.get("project", {}).get("name", ""),
        "description": timeline.get("project", {}).get("description", ""),
        "author": {
            "@type": "Person",
            "name": timeline.get("author", {}).get("name", ""),
            "affiliation": timeline.get("author", {}).get("affiliation", ""),
            "orcid": timeline.get("author", {}).get("orcid", "")
        },
        "dateCreated": timeline.get("created_at"),
        "dateModified": timeline.get("updated_at"),
        "hasPart": []
    }
    
    for event in timeline.get("events", []):
        event_obj = {
            "@type": "ResearchEvent",
            "identifier": event["id"],
            "name": event["description"],
            "startDate": event["date"],
            "eventType": event["type"],
            "description": event["description"]
        }
        if event.get("metrics"):
            event_obj["measurementTechnique"] = ", ".join(f"{k}: {v}" for k, v in event.get("metrics", {}).items() if v is not None)
        context["hasPart"].append(event_obj)
    
    return json.dumps(context, indent=2, ensure_ascii=False)


def export_html(timeline: dict) -> str:
    """Export as interactive HTML widget."""
    html = """<!DOCTYPE html>
<html>
<head>
    <title>Research Timeline</title>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <style>
        body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif; max-width: 800px; margin: 0 auto; padding: 20px; }
        .timeline { position: relative; padding: 20px 0; }
        .event { position: relative; padding: 15px; margin: 10px 0; background: #1a1f2a; border-radius: 8px; border-left: 4px solid #6fc3df; }
        .event-id { font-family: monospace; color: #6fc3df; font-weight: bold; }
        .event-date { color: #8892a8; font-size: 0.9em; }
        .event-desc { color: #e0e4ee; margin: 8px 0; }
        .event-metrics { color: #facc15; font-family: monospace; font-size: 0.85em; }
        .event-tags { margin-top: 8px; }
        .tag { display: inline-block; background: rgba(111,195,223,0.12); color: #6fc3df; padding: 2px 8px; border-radius: 12px; font-size: 0.75em; margin-right: 4px; }
    </style>
</head>
<body>
    <h1>Research Timeline</h1>
    <div class="timeline">"""
    
    for event in timeline.get("events", []):
        metrics = event.get("metrics", {})
        metrics_html = ""
        if event.get("metrics"):
            metrics_html = f'<div class="event-metrics">{" | ".join(f"{k}={v}" for k, v in event["metrics"].items() if v is not None)}</div>'
        
        tags_html = ""
        if event.get("tags"):
            tags_html = '<div class="event-tags">' + "".join(f'<span class="tag">{t}</span>' for t in event["tags"]) + '</div>'
        
        html += f"""
        <div class="event">
            <div class="event-id">{event['id']}</div>
            <div class="event-date">{event['date']}</div>
            <div class="event-desc">{event['description']}</div>
            {metrics_html}
            {tags_html}
        </div>"""
    
    html += """    </div>
</body>
</html>"""
    return html


@app.command()
def validate(
    timeline_file: Path = typer.Option(Path(".research-timeline.json"), "--file", "-f", help="Timeline file"),
):
    """Validate timeline against schema."""
    if not Path(timeline_file).exists():
        print(f"[ERROR] Timeline file not found: {timeline_file}")
        raise typer.Exit(1)
    
    with open(timeline_file, 'r', encoding='utf-8') as f:
        timeline = json.load(f)
    
    # Basic validation
    errors = []
    if "project" not in timeline:
        errors.append("Missing 'project' section")
    if "author" not in timeline:
        errors.append("Missing 'author' section")
    if "events" not in timeline or not timeline["events"]:
        errors.append("Missing or empty 'events' section")
    
    for i, event in enumerate(timeline.get("events", [])):
        if "id" not in event:
            errors.append(f"Event {i}: missing 'id'")
        if "type" not in event:
            errors.append(f"Event {event.get('id', i)}: missing 'type'")
        if "date" not in event:
            errors.append(f"Event {event.get('id', i)}: missing 'date'")
    
    if errors:
        print("[ERROR] Validation failed:")
        for err in errors:
            print(f"  [ERROR] {err}")
        raise typer.Exit(1)
    else:
        print("[OK] Timeline is valid!")


if __name__ == "__main__":
    app()
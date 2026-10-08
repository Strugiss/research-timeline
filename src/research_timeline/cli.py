"""research-timeline CLI.

Track, validate, and export research timelines — from first AI interaction to
scientific discovery. Commands: ``init``, ``log``, ``list``, ``export``,
``stats``, ``validate``; formats: LaTeX, Markdown, standalone HTML, schema.org
JSON-LD, W3C PROV-O (JSON-LD), CSV, and TikZ Gantt.
"""

import html
import json
import re
from datetime import date
from pathlib import Path
from typing import List, Optional

import typer

VALID_EVENT_ID = re.compile(r"^T([0-9]+|n)$|^(pivot|control|submission|publication|milestone)$")

app = typer.Typer(
    name="research-timeline",
    help="Track, visualize, and export research timelines from first AI interaction to scientific discovery",
    add_completion=False,
    no_args_is_help=True,
)

# Default timeline file
DEFAULT_TIMELINE_FILE = Path(".research-timeline.json")

_SCHEMA_CANDIDATES = (
    Path(__file__).resolve().parent / "timeline.schema.json",                 # packaged copy
    Path(__file__).resolve().parents[2] / "schema" / "timeline.schema.json",  # repo copy
)

# LaTeX special characters (escaped in table/Gantt exports)
_LATEX_SPECIAL = {
    "\\": r"\textbackslash{}",
    "&": r"\&", "%": r"\%", "$": r"\$", "#": r"\#", "_": r"\_",
    "{": r"\{", "}": r"\}", "~": r"\textasciitilde{}", "^": r"\textasciicircum{}",
}


def latex_escape(value: object) -> str:
    """Escape LaTeX special characters in user-provided text.

    Args:
        value: Text to escape (any object; converted with ``str``).

    Returns:
        The text with LaTeX special characters replaced by their escapes.
    """
    return "".join(_LATEX_SPECIAL.get(ch, ch) for ch in str(value))


def load_schema() -> dict:
    """Load the packaged JSON Schema (draft-07).

    Searches the packaged copy first, then the repository ``schema/`` copy.

    Returns:
        The parsed schema as a dictionary.

    Raises:
        FileNotFoundError: If no schema copy can be found.
    """
    for candidate in _SCHEMA_CANDIDATES:
        if candidate.is_file():
            with open(candidate, "r", encoding="utf-8") as f:
                return json.load(f)
    raise FileNotFoundError(
        "timeline.schema.json not found (packaged copy or repo schema/)")


def validate_timeline(timeline: dict) -> List[str]:
    """Validate a timeline against the JSON Schema.

    Args:
        timeline: Parsed timeline document.

    Returns:
        A list of human-readable problems (empty when the timeline is valid).
    """
    from jsonschema import Draft7Validator
    validator = Draft7Validator(load_schema(),
                                format_checker=Draft7Validator.FORMAT_CHECKER)
    problems = []
    for err in sorted(validator.iter_errors(timeline),
                      key=lambda e: [str(p) for p in e.absolute_path]):
        where = "/".join(str(p) for p in err.absolute_path) or "(root)"
        problems.append(f"{where}: {err.message}")
    return problems


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
    force: bool = typer.Option(False, "--force", help="Overwrite an existing file without asking"),
):
    """Create a new timeline file with project and author metadata."""
    output_path = Path(output)
    if output_path.exists() and not force:
        if not typer.confirm(f"'{output}' already exists. Overwrite?"):
            print("[ERROR] Aborted: file exists (use --force to overwrite)")
            raise typer.Exit(1)

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
    """Log a new typed event to the timeline.

    The event ID must be unique and match the typed phases (``T0``…``Tn``,
    ``pivot``, ``control``, ``submission``, ``publication``, ``milestone``).
    The resulting document is validated against the JSON Schema before it is
    written; invalid events are rejected without touching the file.
    """
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
    for existing in timeline.get("events", []):
        if existing.get("id") == event_id:
            print(f"[ERROR] Event ID {event_id} already exists")
            raise typer.Exit(1)

    # Build event
    event: dict = {
        "id": event_id,
        "type": event_type,
        "date": event_date,
        "description": description,
        "tags": [t.strip() for t in tags.split(",")] if tags else [],
    }
    if end_date:
        event["end_date"] = end_date

    # Add metrics if provided
    metrics: dict = {}
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
    evidence: dict = {}
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

    problems = validate_timeline(timeline)
    if problems:
        print("[ERROR] Event rejected by schema validation:")
        for problem in problems:
            print(f"  [ERROR] {problem}")
        raise typer.Exit(1)

    with open(timeline_file, 'w', encoding='utf-8') as f:
        json.dump(timeline, f, indent=2, ensure_ascii=False)

    print(f"[OK] Logged event {event_id}: {description}")


@app.command()
def edit(
    event_id: str = typer.Argument(..., help="Event ID to edit"),
    description: Optional[str] = typer.Option(None, "--desc", help="New description"),
    event_date: Optional[str] = typer.Option(None, "--date", help="New date (YYYY-MM-DD)"),
    end_date: Optional[str] = typer.Option(None, "--end-date", help="New end date (YYYY-MM-DD)"),
    tags: Optional[str] = typer.Option(None, "--tags", help="New tags (comma-separated)"),
    timeline_file: Path = typer.Option(Path(".research-timeline.json"), "--file", "-f", help="Timeline file"),
):
    """Edit fields of an existing event (description, date, end date, tags).

    Only the fields you pass are changed. The document is validated against
    the JSON Schema before it is written.
    """
    if description is None and event_date is None and end_date is None and tags is None:
        print("[ERROR] Nothing to update (pass at least one field)")
        raise typer.Exit(1)
    if not Path(timeline_file).exists():
        print(f"[ERROR] Timeline file not found: {timeline_file}")
        raise typer.Exit(1)

    with open(timeline_file, 'r', encoding='utf-8') as f:
        timeline = json.load(f)

    target = None
    for existing in timeline.get("events", []):
        if existing.get("id") == event_id.strip():
            target = existing
            break
    if target is None:
        print(f"[ERROR] Event ID {event_id} not found")
        raise typer.Exit(1)

    if description is not None:
        target["description"] = description
    if event_date is not None:
        target["date"] = event_date
    if end_date is not None:
        target["end_date"] = end_date
    if tags is not None:
        target["tags"] = [t.strip() for t in tags.split(",") if t.strip()]
    timeline["updated_at"] = str(date.today())

    problems = validate_timeline(timeline)
    if problems:
        print("[ERROR] Edit rejected by schema validation:")
        for problem in problems:
            print(f"  [ERROR] {problem}")
        raise typer.Exit(1)

    with open(timeline_file, 'w', encoding='utf-8') as f:
        json.dump(timeline, f, indent=2, ensure_ascii=False)
    print(f"[OK] Event {event_id} updated")


@app.command()
def remove(
    event_id: str = typer.Argument(..., help="Event ID to remove"),
    yes: bool = typer.Option(False, "--yes", "-y", help="Skip the confirmation prompt"),
    timeline_file: Path = typer.Option(Path(".research-timeline.json"), "--file", "-f", help="Timeline file"),
):
    """Remove an event from the timeline (asks for confirmation)."""
    if not Path(timeline_file).exists():
        print(f"[ERROR] Timeline file not found: {timeline_file}")
        raise typer.Exit(1)

    with open(timeline_file, 'r', encoding='utf-8') as f:
        timeline = json.load(f)

    events = timeline.get("events", [])
    remaining = [e for e in events if e.get("id") != event_id.strip()]
    if len(remaining) == len(events):
        print(f"[ERROR] Event ID {event_id} not found")
        raise typer.Exit(1)
    if not yes and not typer.confirm(f"Remove event {event_id}?"):
        print("[ERROR] Aborted: event not removed")
        raise typer.Exit(1)

    timeline["events"] = remaining
    timeline["updated_at"] = str(date.today())

    problems = validate_timeline(timeline)
    if problems:
        print("[ERROR] Removal rejected by schema validation:")
        for problem in problems:
            print(f"  [ERROR] {problem}")
        raise typer.Exit(1)

    with open(timeline_file, 'w', encoding='utf-8') as f:
        json.dump(timeline, f, indent=2, ensure_ascii=False)
    print(f"[OK] Event {event_id} removed")


@app.command()
def list(
    timeline_file: Path = typer.Option(Path(".research-timeline.json"), "--file", "-f", help="Timeline file"),
    show_metrics: bool = typer.Option(False, "--metrics", "-m", help="Show metrics"),
    event_type: Optional[str] = typer.Option(None, "--type", help="Filter by event type"),
    tag: Optional[str] = typer.Option(None, "--tag", help="Filter by tag (exact match)"),
    since: Optional[str] = typer.Option(None, "--since", help="Only events with date >= YYYY-MM-DD"),
    until: Optional[str] = typer.Option(None, "--until", help="Only events with date <= YYYY-MM-DD"),
    json_out: bool = typer.Option(False, "--json", help="Output the filtered events as JSON"),
):
    """List events, with optional filters by type, tag, or date window."""
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

    if json_out:
        print(json.dumps(events, indent=2, ensure_ascii=False))
        return

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
    format: str = typer.Option(
        "latex", "--format",
        help="Export format: latex, markdown, jsonld, html, csv, gantt, prov"),
    timeline_file: Path = typer.Option(Path(".research-timeline.json"), "--file", help="Timeline file"),
    output: Optional[Path] = typer.Option(None, "--output", "-o", help="Output file"),
):
    """Export the timeline to LaTeX, Markdown, HTML, JSON-LD, PROV-O, CSV, or Gantt (TikZ)."""
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
    elif format == "prov":
        output_content = export_prov(timeline)
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
    """Export the timeline as CSV (machine-readable, spreadsheet-friendly).

    Args:
        timeline: Parsed timeline document.

    Returns:
        CSV content as a single string (header + one row per event).
    """
    import builtins
    import csv
    import io
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
    """Export the timeline as a publication-ready Gantt chart (LaTeX TikZ).

    Requires ``\\usepackage{tikz}``. Point events render as markers; events
    with an ``end_date`` render as bars.

    Args:
        timeline: Parsed timeline document.

    Returns:
        TikZ content as a single string.
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
        desc = latex_escape(str(e["description"])[:40])
        # label on the left
        lines.append(f"  \\node[anchor=east,align=right] at (0,{y:.2f}) "
                     f"{{{latex_escape(e['id'])} \\textsc{{{latex_escape(e['type'])}}}}};")
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
    json_out: bool = typer.Option(False, "--json", help="Output statistics as JSON"),
):
    """Print summary statistics: event count, date window, per-type and per-tag counts."""
    if not Path(timeline_file).exists():
        print(f"[ERROR] Timeline file not found: {timeline_file}")
        raise typer.Exit(1)

    with open(timeline_file, 'r', encoding='utf-8') as f:
        timeline = json.load(f)

    events = timeline.get("events", [])
    if not events:
        print("No events recorded.")
        raise typer.Exit(0)

    types: dict = {}
    for e in events:
        t = e.get("type", "?")
        types[t] = types.get(t, 0) + 1

    tags: dict = {}
    for e in events:
        for tg in e.get("tags", []):
            tags[tg] = tags.get(tg, 0) + 1

    dates = [e.get("date", "") for e in events if e.get("date")]
    d0 = min(dates)
    d1 = max(dates)
    try:
        window_days = (date.fromisoformat(d1) - date.fromisoformat(d0)).days
    except ValueError:
        window_days = 0

    if json_out:
        print(json.dumps({
            "events": len(events),
            "date_window": {"start": d0, "end": d1, "days": window_days},
            "by_type": dict(sorted(types.items())),
            "by_tag": dict(sorted(tags.items())),
        }, indent=2, ensure_ascii=False))
        return

    print(f"Events:      {len(events)}")
    print(f"Date window: {d0} .. {d1} ({window_days} days)")
    print("By type:")
    for t, c in sorted(types.items()):
        print(f"  {t:<14} {c}")
    print("By tag:")
    for tg, c in sorted(tags.items()):
        print(f"  {tg:<14} {c}")


def export_latex(timeline: dict) -> str:
    """Export the timeline as a LaTeX table (manuscript-ready).

    Args:
        timeline: Parsed timeline document.

    Returns:
        The ``table`` environment as a single string.
    """
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
            f"{latex_escape(event['id'])} & {latex_escape(event['date'])} & "
            f"{latex_escape(str(event['description'])[:50])} & "
            f"{latex_escape(metrics_str)} & {latex_escape(evidence_str)} \\\\"
        )

    lines.extend([
        "\\bottomrule",
        "\\end{tabular}",
        "\\end{table}",
    ])
    return "\n".join(lines)


def export_markdown(timeline: dict) -> str:
    """Export the timeline as a Markdown table (portable, README-friendly).

    Args:
        timeline: Parsed timeline document.

    Returns:
        The table as Markdown text.
    """
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
    """Export the timeline as schema.org JSON-LD (``ResearchProject`` + ``Event``).

    Args:
        timeline: Parsed timeline document.

    Returns:
        The JSON-LD document as a string.
    """
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
            "@type": "Event",
            "identifier": event["id"],
            "name": event["description"],
            "startDate": event["date"],
            "description": event["description"]
        }
        if event.get("end_date"):
            event_obj["endDate"] = event["end_date"]
        if event.get("tags"):
            event_obj["keywords"] = event["tags"]
        if event.get("metrics"):
            event_obj["additionalProperty"] = [
                {"@type": "PropertyValue", "name": k, "value": v}
                for k, v in event["metrics"].items() if v is not None
            ]
        context["hasPart"].append(event_obj)

    return json.dumps(context, indent=2, ensure_ascii=False)


def export_prov(timeline: dict) -> str:
    """Export the timeline as a W3C PROV-O provenance graph (JSON-LD).

    Mapping: project → ``prov:Bundle``; author → ``prov:Person``; declared AI
    role → ``prov:SoftwareAgent``; events → ``prov:Activity`` (ISO start/end
    times) associated with both agents; evidence items → ``prov:Entity``
    generated by their event. Custom ``rt:`` terms carry metrics, tags, type.

    Args:
        timeline: Parsed timeline document.

    Returns:
        The PROV-O JSON-LD document as a string.
    """
    project = timeline.get("project", {})
    author = timeline.get("author", {})
    name = project.get("name", "research-timeline")
    slug = re.sub(r"[^A-Za-z0-9_-]+", "-", str(name)).strip("-").lower() or "project"
    base = f"urn:research-timeline:{slug}"
    ai_role = author.get("ai_role")

    author_entry = {
        "@id": f"{base}:agent:author",
        "@type": "prov:Person",
        "prov:label": author.get("name", ""),
        "rt:affiliation": author.get("affiliation", ""),
    }
    if author.get("orcid"):
        author_entry["rt:orcid"] = author["orcid"]

    graph = [
        {
            "@id": base,
            "@type": "prov:Bundle",
            "prov:label": name,
            "rt:description": project.get("description", ""),
            "rt:domain": project.get("domain", ""),
        },
        author_entry,
    ]
    if ai_role:
        graph.append({
            "@id": f"{base}:agent:ai",
            "@type": "prov:SoftwareAgent",
            "rt:role": ai_role,
        })

    agents = [f"{base}:agent:author"]
    if ai_role:
        agents.append(f"{base}:agent:ai")

    for event in timeline.get("events", []):
        eid = f"{base}:event:{event.get('id', '?')}"
        activity = {
            "@id": eid,
            "@type": "prov:Activity",
            "prov:label": event.get("description", ""),
            "prov:startedAtTime": {"@value": event.get("date", ""), "@type": "xsd:date"},
            "prov:wasAssociatedWith": agents,
        }
        if event.get("end_date"):
            activity["prov:endedAtTime"] = {"@value": event["end_date"], "@type": "xsd:date"}
        for key in ("type", "tags", "metrics"):
            if event.get(key):
                activity[f"rt:{key}"] = event[key]
        graph.append(activity)
        evidence = event.get("evidence") or {}
        for kind, value in evidence.items():
            if value:
                graph.append({
                    "@id": f"{eid}:evidence:{kind}",
                    "@type": "prov:Entity",
                    "rt:kind": kind,
                    "rt:value": value,
                    "prov:wasGeneratedBy": eid,
                })

    doc = {
        "@context": {
            "prov": "http://www.w3.org/ns/prov#",
            "rt": "https://github.com/Strugiss/research-timeline#",
            "xsd": "http://www.w3.org/2001/XMLSchema#",
        },
        "@graph": graph,
    }
    return json.dumps(doc, indent=2, ensure_ascii=False)


def export_html(timeline: dict) -> str:
    """Export the timeline as a standalone HTML widget (no build step).

    Args:
        timeline: Parsed timeline document.

    Returns:
        The HTML document as a single string.
    """
    out = """<!DOCTYPE html>
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
        metrics_html = ""
        if event.get("metrics"):
            metrics_txt = " | ".join(f"{k}={v}" for k, v in event["metrics"].items() if v is not None)
            metrics_html = f'<div class="event-metrics">{html.escape(metrics_txt)}</div>'

        tags_html = ""
        if event.get("tags"):
            tags_html = ('<div class="event-tags">'
                         + "".join(f'<span class="tag">{html.escape(str(t))}</span>'
                                   for t in event["tags"])
                         + '</div>')

        out += f"""
        <div class="event">
            <div class="event-id">{html.escape(str(event['id']))}</div>
            <div class="event-date">{html.escape(str(event['date']))}</div>
            <div class="event-desc">{html.escape(str(event['description']))}</div>
            {metrics_html}
            {tags_html}
        </div>"""

    out += """    </div>
</body>
</html>"""
    return out


@app.command()
def validate(
    timeline_file: Path = typer.Option(Path(".research-timeline.json"), "--file", "-f", help="Timeline file"),
):
    """Validate the timeline against the shipped JSON Schema (draft-07)."""
    if not Path(timeline_file).exists():
        print(f"[ERROR] Timeline file not found: {timeline_file}")
        raise typer.Exit(1)

    try:
        with open(timeline_file, 'r', encoding='utf-8') as f:
            timeline = json.load(f)
    except json.JSONDecodeError as exc:
        print(f"[ERROR] Invalid JSON: {exc}")
        raise typer.Exit(1)

    problems = validate_timeline(timeline)
    if problems:
        print("[ERROR] Validation failed:")
        for problem in problems:
            print(f"  [ERROR] {problem}")
        raise typer.Exit(1)
    print("[OK] Timeline is valid!")


if __name__ == "__main__":
    app()

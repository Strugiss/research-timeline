# Research Timeline

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.21855315.svg)](https://doi.org/10.5281/zenodo.21855315)
[![CI](https://github.com/Strugiss/research-timeline/actions/workflows/ci.yml/badge.svg)](https://github.com/Strugiss/research-timeline/actions/workflows/ci.yml)
[![Python](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![SWH](https://archive.softwareheritage.org/badge/swh:1:snp:62a2f748e52113016cf291c4b8c944e86c6848bf/)](https://archive.softwareheritage.org/swh:1:snp:62a2f748e52113016cf291c4b8c944e86c6848bf)

Track, visualize, and export research timelines — from first AI interaction to scientific discovery.

> **RETTIFICA (01/09/2026)**: una precedente asserzione di unicità di questo
> strumento è stata formulata senza una verifica di mercato documentata. La
> verifica del 01/09/2026 ha evidenziato strumenti simili esistenti
> (timeline-fishbone-generator, timeline-maker, SubThesis Timeline Generator,
> Research-Timeline-Planner, The Timeline Project, altri). Questo strumento non
> è unico: si distingue per tracciamento AI→scoperta, evidence QPU e disclosure
> `ai_role`, ma la sua esistenza non è isolata.

`research-timeline` documents the **process** of research, not just its artifacts: every milestone of a project (the first AI interaction that shaped the protocol, the first QPU commit with its evidence, pivots, controls, submissions, publications) is recorded in a single versioned JSON file with typed events, quantitative metrics, and supporting evidence.

## Features

- **Typed events** — `T0`, `T1`…`Tn`, `pivot`, `control`, `submission`, `publication`, `milestone`
- **Metrics** — attach any quantitative result (z-scores, shots, backend, MI, …) to an event
- **Evidence** — git commits, IBM Quantum job IDs, data links, code links
- **AI-role disclosure** — each timeline declares how AI was used (`cognitive_prosthesis`, `co_pilot`, `autonomous_agent`)
- **Exports** — LaTeX table (papers/reports), Markdown, standalone HTML, schema.org JSON-LD, CSV, publication-ready Gantt (TikZ)
- **Filters** — list events by type, tag, or date window (`--type`, `--tag`, `--since`, `--until`)
- **Stats** — duration window, per-type and per-tag counts (`stats`)
- **Date ranges** — optional `--end-date` turns a point event into a range (rendered as a bar in the Gantt)
- **Validate** — structural checks with CI-friendly exit codes
- **Simple JSON storage** — human readable, diff-friendly, git-native, zero lock-in

## Installation

```bash
pip install -e .
# or from the archive:
pip install git+https://github.com/Strugiss/research-timeline.git
```

## Usage

```bash
# Initialize a timeline
research-timeline init --output timeline.json

# Log a typed event (with metrics and evidence)
research-timeline log T1 --desc "First commit: 14 QPU experiments, Z>50sigma" \
  --z-combined 50.0 --git-commit c3ddc4a --job-ids abc,def --tags commit,qpu

# List events (optionally with metrics, filters)
research-timeline list --metrics
research-timeline list --type milestone --tag qpu --since 2026-01-01 --until 2026-12-31

# Summary statistics (duration, per-type, per-tag)
research-timeline stats

# Export to LaTeX (papers), Markdown, HTML, JSON-LD, CSV, or Gantt (TikZ)
research-timeline export --format latex -o timeline.tex
research-timeline export --format markdown -o timeline.md
research-timeline export --format html -o timeline.html
research-timeline export --format jsonld -o timeline.jsonld
research-timeline export --format csv -o timeline.csv
research-timeline export --format gantt -o timeline_gantt.tex   # publication-ready TikZ

# Validate
research-timeline validate
```

See [example/timeline.json](example/timeline.json) for a real-world timeline
(the PASM DTC Discovery project, N47Lab MatterMemory research program) and the
generated exports in `example/`.

## Event IDs

`T0`, `T1`, `T2`, …, `Tn` (ordered research phases) plus special events:
`pivot`, `control`, `submission`, `publication`, `milestone`.

## File Format

A timeline is a single JSON document:

```json
{
  "project": {"name": "PASM DTC Discovery", "description": "...", "domain": "quantum"},
  "author": {"name": "N47Lab", "affiliation": "independent", "ai_role": "cognitive_prosthesis"},
  "events": [{
    "id": "T1", "type": "T1", "date": "2026-07-31",
    "description": "First commit: 14 QPU experiments, Z>50sigma",
    "metrics": {"z_score_combined": 50.0},
    "evidence": {"git_commit": "c3ddc4a", "job_ids": ["abc"]}
  }]
}
```

The schema is documented in `schema/timeline.schema.json` (JSON Schema draft-07).

## Development & Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) — tests, coding conventions, and governance.

```bash
pip install -e ".[dev]"
pytest tests/ -v
```

## Software Heritage

This repository is archived in permanent storage:
`swh:1:snp:62a2f748e52113016cf291c4b8c944e86c6848bf`

## License

MIT — see [LICENSE](LICENSE).
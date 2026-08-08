# Research Timeline

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.21830143.svg)](https://doi.org/10.5281/zenodo.21830143)
[![CI](https://github.com/Strugiss/research-timeline/actions/workflows/ci.yml/badge.svg)](https://github.com/Strugiss/research-timeline/actions/workflows/ci.yml)
[![Python](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![SWH](https://archive.softwareheritage.org/badge/swh:1:snp:62a2f748e52113016cf291c4b8c944e86c6848bf/)](https://archive.softwareheritage.org/swh:1:snp:62a2f748e52113016cf291c4b8c944e86c6848bf)

Track, visualize, and export research timelines â€” from first AI interaction to scientific discovery.

`research-timeline` documents the **process** of research, not just its artifacts: every milestone of a project (the first AI interaction that shaped the protocol, the first QPU commit with its evidence, pivots, controls, submissions, publications) is recorded in a single versioned JSON file with typed events, quantitative metrics, and supporting evidence.

## Features

- **Typed events** â€” `T0`, `T1`â€¦`Tn`, `pivot`, `control`, `submission`, `publication`, `milestone`
- **Metrics** â€” attach any quantitative result (z-scores, shots, backend, MI, â€¦) to an event
- **Evidence** â€” git commits, IBM Quantum job IDs, data links, code links
- **AI-role disclosure** â€” each timeline declares how AI was used (`cognitive_prosthesis`, `co_pilot`, `autonomous_agent`)
- **Exports** â€” LaTeX table (papers/reports), Markdown, standalone HTML, schema.org JSON-LD
- **Validate** â€” structural checks with CI-friendly exit codes
- **Simple JSON storage** â€” human readable, diff-friendly, git-native, zero lock-in

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

# List events (optionally with metrics)
research-timeline list --metrics

# Export to LaTeX (papers), Markdown, HTML, or JSON-LD
research-timeline export --format latex -o timeline.tex
research-timeline export --format markdown -o timeline.md
research-timeline export --format html -o timeline.html
research-timeline export --format jsonld -o timeline.jsonld

# Validate
research-timeline validate
```

See [example/timeline.json](example/timeline.json) for a real-world timeline
(the PASM DTC Discovery project, N47Lab MatterMemory research program) and the
generated exports in `example/`.

## Event IDs

`T0`, `T1`, `T2`, â€¦, `Tn` (ordered research phases) plus special events:
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

See [CONTRIBUTING.md](CONTRIBUTING.md) â€” tests, coding conventions, and governance.

```bash
pip install -e ".[dev]"
pytest tests/ -v
```

## Software Heritage

This repository is archived in permanent storage:
`swh:1:snp:62a2f748e52113016cf291c4b8c944e86c6848bf`

## License

MIT â€” see [LICENSE](LICENSE).
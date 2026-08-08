# Research Timeline

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.21830143.svg)](https://doi.org/10.5281/zenodo.21830143)
[![CI](https://github.com/Strugiss/research-timeline/actions/workflows/ci.yml/badge.svg)](https://github.com/Strugiss/research-timeline/actions/workflows/ci.yml)
[![Python](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![SWH](https://archive.softwareheritage.org/badge/swh:1:snp:33902e719a13fb12e199524c923e66cad65aeda/)](https://archive.softwareheritage.org/swh:1:snp:339028719a13fb1de3d99524c923e66cad65aeda)

A zero-dependency CLI tool for tracking research progress — designed for independent researchers and small groups.

## Features

- **Log entries** with date, title, status, tags, notes
- **List/filter** by status or tags
- **Export** to YAML, JSON, or Markdown
- **Validate** timeline integrity (CI-friendly exit codes)
- **Simple YAML storage** — human readable, diff-friendly, git-native

## Installation

```bash
pip install -e .
# or from the archive:
pip install git+https://github.com/Strugiss/research-timeline.git
```

## Usage

```bash
# Initialize timeline
research-timeline init

# Log entries
research-timeline log "Started literature review" -s in_progress -t "literature,review"
research-timeline log "Completed first draft" -s completed -t "writing" -n "5000 words"

# List entries
research-timeline list
research-timeline list -s completed
research-timeline list -t literature

# Export
research-timeline export -F md -o timeline.md
research-timeline export -F json

# Validate
research-timeline validate
```

## Status Values

- `pending` — not started
- `in_progress` — actively working
- `completed` — done
- `cancelled` — abandoned

## File Format

```yaml
entries:
  - date: "2024-01-15"
    title: "Literature review on quantum DTCs"
    status: completed
    tags: [literature, quantum, dtc]
    notes: "Covered 47 papers, identified 3 key gaps"
  - date: "2024-01-20"
    title: "Design PASM circuit"
    status: in_progress
    tags: [circuit, pasm]
    notes: "Testing 3-qubit variant"
```

The file is plain YAML — every part of the research workflow can read it, diff it, and version it.

## Development & Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) — tests, coding conventions, and governance.

```bash
pip install -e ".[dev]"
pytest tests/ -v
```

## Software Heritage

This repository is archived in permanent storage:
`swh:1:snp:339028719a13fb1de3d99524c923e66cad65aeda`

## License

MIT — see [LICENSE](LICENSE).
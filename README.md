# research-timeline

**Track, visualize, and export research timelines — from first AI interaction to scientific discovery.**

[![CI](https://github.com/Strugiss/research-timeline/actions/workflows/ci.yml/badge.svg)](https://github.com/Strugiss/research-timeline/actions/workflows/ci.yml)
[![PyPI](https://img.shields.io/pypi/v/research-timeline)](https://pypi.org/project/research-timeline/)
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.21862618.svg)](https://doi.org/10.5281/zenodo.21862618)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python](https://img.shields.io/badge/python-3.9%2B-blue.svg)](https://www.python.org/)

`research-timeline` documents the **process** of research, not just its artifacts: every milestone of a project (the first AI interaction that shaped the protocol, the first QPU commit with its evidence, pivots, controls, submissions, publications) is recorded in a single versioned JSON file with typed events, quantitative metrics, and supporting evidence.

> **RETTIFICA (01/09/2026)**: una precedente asserzione di unicità di questo
> strumento è stata formulata senza una verifica di mercato documentata. La
> verifica del 01/09/2026 ha evidenziato strumenti simili esistenti
> (timeline-fishbone-generator, timeline-maker, SubThesis Timeline Generator,
> Research-Timeline-Planner, The Timeline Project, altri). Questo strumento non
> è unico: si distingue per tracciamento AI→scoperta, evidence QPU e disclosure
> `ai_role`, ma la sua esistenza non è isolata.

## Terminal preview

Real output (v0.2.4, Typer + rich):

```console
$ research-timeline init -n "PASM DTC Discovery" -d "Classical prethermal DTC via PASM on IBM Quantum" -a "Alessandro Tulli" -o timeline.json
[OK] Initialized timeline at timeline.json
  Project: PASM DTC Discovery (quantum)
  Author: Alessandro Tulli (without academic degrees)

$ research-timeline log T1 --type T1 --desc "First QPU campaign: 14 experiments, Z>50 sigma" --z-combined 50.0 --backend ibm_kingston --job-ids abc123,def456 --tags commit,qpu -f timeline.json
[OK] Logged event T1: First QPU campaign: 14 experiments, Z>50 sigma

$ research-timeline validate -f timeline.json
[OK] Timeline is valid!

$ research-timeline stats -f timeline.json
Events:      1
Date window: 2026-09-14 .. 2026-09-14 (0 days)
By type:
  T1             1
By tag:
  commit         1
  qpu            1
```

## Features

| Feature | Description |
|---|---|
| **Typed events** | `T0`, `T1`…`Tn` (ordered research phases) plus `pivot`, `control`, `submission`, `publication`, `milestone` |
| **Metrics & evidence** | Attach z-scores, shots, backends, IBM Quantum job IDs, git commits, data/code links to any event |
| **AI-role disclosure** | Each timeline declares how AI was used: `cognitive_prosthesis`, `co_pilot`, `autonomous_agent` |
| **Exports** | LaTeX table (papers/reports), Markdown, standalone HTML, schema.org JSON-LD, CSV, publication-ready Gantt (TikZ) |
| **JSON Schema draft-07** | Machine-readable schema (`schema/timeline.schema.json`) with `validate` and CI-friendly exit codes |
| **Filters & stats** | `--type`, `--tag`, `--since`, `--until`; duration window, per-type and per-tag counts |
| **Date ranges** | `--end-date` turns a point event into a range (rendered as a bar in the Gantt) |
| **Git-native storage** | One human-readable, diff-friendly JSON file — zero lock-in |

## Install

```bash
pip install research-timeline
```

## Quick start (3 steps)

```bash
# 1) initialize a timeline
research-timeline init -n "My project" -d "What the research is about" -a "Your Name" -o timeline.json

# 2) log a typed event with metrics and evidence
research-timeline log T1 --type T1 --desc "First result" --z-score 5.0 --git-commit abc1234 --tags result -f timeline.json

# 3) export (latex | markdown | html | jsonld | csv | gantt)
research-timeline export --format latex -o timeline.tex --file timeline.json
```

See [`example/timeline.json`](example/timeline.json) for a real-world timeline
(the PASM DTC Discovery project, N47Lab MatterMemory research program) and the
generated exports in `example/`.

## Documentation

Full documentation: **https://strugiss.github.io/research-timeline/** — install, commands, file format, exports, FAQ.

## Community & archive

- pyOpenSci software submission: [issue #338](https://github.com/pyOpenSci/software-submission/issues/338)
- Archived on Zenodo: [10.5281/zenodo.21862618](https://doi.org/10.5281/zenodo.21862618)
- Software Heritage: `swh:1:snp:62a2f748e52113016cf291c4b8c944e86c6848bf`

## Links

- N47Lab main site: https://n47lab.altervista.org/
- Source code: https://github.com/Strugiss/research-timeline

## License

MIT — see [LICENSE](LICENSE).

## Contributing

Contributions are welcome: see [CONTRIBUTING.md](CONTRIBUTING.md) for tests, coding conventions, and governance.

```bash
pip install -e ".[dev]"
pytest tests/ -v
```

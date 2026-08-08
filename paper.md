---
title: "research-timeline: A CLI tool for tracking the research process from first AI interaction to paper"
authors:
  - name: Alessandro Tulli
    affiliation: "N47Lab"
    orcid: "0009-0008-9201-6080"
date: 2026-08-09
version: "v0.2.0"
doi: "10.5281/zenodo.21830143"
repository: "https://github.com/Strugiss/research-timeline"
archive_doi: "10.5281/zenodo.21830143"
---

# Summary

`research-timeline` is a command-line tool that records the **process** of a research project — from the first AI interaction that shaped the idea to the final submission and publication — as a structured, versioned JSON timeline. Each event is typed (`T0`–`Tn` for ordered research phases, plus `pivot`, `control`, `submission`, `publication`, `milestone`), carries quantitative **metrics** (e.g., combined z-scores, shots, QPU backend), and **evidence** (git commit hashes, quantum-computing job IDs, data links, code links). The timeline lives as a single plain-JSON file inside the project repository, diffs cleanly with `git`, passes CI validation, and exports to LaTeX tables, Markdown, standalone HTML, or schema.org JSON-LD. It is deliberately minimal, offline-friendly, and free of cloud lock-in.

# Statement of Need

Independent researchers and small groups lack lightweight tooling to record *how* a result was produced — the design decisions, AI-assisted steps, failed experiments, controls, and final submission. The reproducibility literature (Baker, 2016) shows that process information is exactly what gets lost when results are shared, because it is scattered across notebooks, chat logs, and emails rather than versioned with the code. Standard task trackers and experiment trackers do not model research phases; nothing records the role of generative AI in the workflow in a machine-readable way.

In the era of AI-assisted research, there is a need for a citable, versionable record that discloses the role AI played (`cognitive_prosthesis`, `co_pilot`, `autonomous_agent`) and anchors each step to verifiable evidence — commits, QPU job IDs, data/code links — so that "how the research happened" is as reproducible as the results themselves. `research-timeline` provides that record with a minimal, CI-friendly, schema-validated tool.

# State of the Field

Existing categories and how this tool differs:

- **Notes/task tools (Notion, Obsidian, Logseq, Trello)** — general-purpose notes, task boards, or graphs; no typed research phases, no JSON schema, no CI validation, and cloud-dependent storage.
- **Experiment trackers (Weights & Biases, MLflow, DVC)** — track model *runs*, artifacts, and metrics; they do not record researcher-level process events (first insight, pivot, control, submission) nor provide paper-oriented exports (LaTeX).
- **Notebooks (Jupyter, Quarto)** — rich narrative but unstructured; no enforcement of a timeline schema, no typed categories, no machine-readable JSON-LD export.
- **Lab notebooks (ELN, Code Ocean)** — heavyweight, instrument-locked, or in the cloud; overkill for a single-author project.

`research-timeline` occupies the empty slot: a zero-dependency, git-native, JSON-backed tracker for the research *narrative* with an explicit schema, education `evidence` fields, and LaTeX/JSON-LD export for downstream writing. It is not another task manager — it is a provenance instrument for the research process.

# Software Design

The tool is a single Python package (Python ≥ 3.9) with a small API surface:

- `research_timeline.cli` — the Typer-based CLI: commands `init`, `log`, `list`, `export`, and `validate`. Pydantic models validate on load/save.
- `research_timeline.models` — Pydantic models (`ProjectInfo`, `Author`, `Event`, `Metrics`, `Evidence`, `ResearchTimeline`) enforcing the data model, including the `ai_role` disclosure field for the author.
- Storage: one JSON document (default `timeline.json`), validated against `schema/timeline.schema.json` (JSON Schema draft-07).
- Typed event IDs: `T0`–`Tn`, `pivot`, `control`, `submission`, `publication`, `milestone`. Invalid or duplicate IDs are rejected at the CLI boundary.
- Metrics and evidence: free-form key/value pairs attached to an event (e.g., `z_score_combined`, `mi_shared`, `shots`, `backend`, `job_ids`, `git_commit`, `data_links`, `code_links`), so any quantitative result of a physics experiment can be anchored to the event.
- Exporters: LaTeX table (`--format latex`), Markdown, standalone HTML, and schema.org JSON-LD (`@type: ResearchProject`) — the timeline can be dropped directly into a paper, a report, or an HTML landing page.
- Engineering trade-off: **simplicity > power** — no database, no cloud, no lock-in. A single file is readable by any JSON parser, diffable in `git`, and durable across decades.

# Research Impact Statement

This tool was used inside the N47Lab MatterMemory research program — a test of sub-planckian phase-imprint dark-matter candidates via phase-anchored-state multiplexing (PASM) on IBM Quantum hardware — to record the full process: the first AI interaction that designed the protocol (T0), the first commit with 14 QPU experiments and combined significance Z > 50σ (T1), the replica study (Z = 39.6σ), the φ-scan pivot, the witness control (no signals), QST/discordance checks, the extension from distance independence (Z = 34σ), the QPU scaling limit (3-qubit peak), and the JOSS submission (2026-08-07). The resulting timeline (`example/timeline.json`) is the authoritative process record of that research, archived with the repository on Software Heritage and an accompanying evidence hyperlink. It is intended as a reusable, tested building for other groups to track their own discovery processes.

# AI Usage Disclosure

This project used AI assistance during script development and documentation drafting (June–August, 2026). All AI-assisted outputs were reviewed line-by-line by the human author; algorithmic behavior is covered by the test suite in `/tests` and CI. The design decisions (schema, event types, export contracts, `ai_role` semantics) were made by the human author, with AI acting as a cognitive prosthesis.

# Installation

```bash
pip install -e .
# or from source:
pip install git+https://github.com/Strugiss/research-timeline.git
```

# Usage

```bash
# Initialize a timeline
research-timeline init --name "DiscoveryX" --output timeline.json

# Log a typed event with metrics and evidence
research-timeline log T1 --desc "First QPU run" --z-combined 50.0 \
  --git-commit c3ddc4a --job-ids abc,def --backend ibm_kingston --file timeline.json

# List events (with metrics)
research-timeline list --metrics --file timeline.json

# Export to LaTeX / Markdown / HTML / JSON-LD
research-timeline export --format latex -o timeline.tex --file timeline.json
research-timeline export --format markdown -o timeline.md --file timeline.json
research-timeline export --format html -o timeline.html --file timeline.json
research-timeline export --format jsonld -o timeline.jsonld --file timeline.json

# Validate
research-timeline validate --file timeline.json
```

Commands default to `--file timeline.json` (path to the timeline file), created by `init`.

# Development

```bash
pip install -e ".[dev]"
pytest tests/ -v       # 14 tests
```

# References

- Baker, M. (2016) "1,500 scientists lift the lid on reproducibility", *Nature* 533, 452–454. doi:10.1038/533452a
- Zenodo archive: 10.5281/zenodo.21830143
- Software Heritage archive: `swh:1:snp:d60633d275c439b3973b506bb00f4b974e62ec0f`
- N47Lab research program (PASM): https://github.com/Strugiss/N47Lab-QuantumResearch
- IBM Quantum: https://quantum.ibm.com
- JSON Schema draft-07: https://json-schema.org
---
title: "research-timeline: A CLI tool for tracking research progress"
authors:
  - name: Alessandro Tulli
    affiliation: "N47Lab"
    orcid: "0009-0008-9201-6080"
date: 2026-08-07
version: "v0.1.1"
doi: "10.5281/zenodo.21830143"
repository: "https://github.com/Strugiss/research-timeline"
archive_doi: "10.5281/zenodo.21830143"
---

# Summary

`research-timeline` is a zero-dependency, git-native command-line tool that lets researchers record, filter, and export the evolution of their research projects as structured, human-readable YAML timelines. It is designed for independent researchers and small groups who want reproducible, portable project histories without institutional infrastructure, cloud lock-in, or heavy task-management software. Timelines are plain files: they version naturally with `git`, diff cleanly, and can be validated programmatically, enabling automated workflows such as progress reports, grant tracking, and research-log preservation.

# Statement of Need

Independent researchers, early-career scientists, and small research groups typically lack lightweight tooling to keep a structured, citable record of research progress. General-purpose solutions in this space fall into two extremes: on one side, enterprise tools (Notion, Jira, Trello) that couple data to proprietary cloud backends and present steep learning curves and no portable storage format; on the other, generic plain-text editors that provide no structure, validation, or query capabilities. Neither class supports the specific needs of research workflows: a minimal, scriptable interface; version-control-friendly storage; an explicit notion of research state; and the ability to export the trajectory of a project (e.g., for a thesis log, a funding report, or a reproducibility appendix).

More concrete design guidance comes from the reproducibility literature (Baker, 2016) which highlights that many research projects lose access to their own process history because recording is fragmented across tools, formats, and locations. `research-timeline` addresses this by persisting the entire project history in a single structured file that lives inside the project repository itself, co-versioned with the code and data it describes. Software Heritage already preserves the four N47Lab research repositories (`swh:1:snp:3390...`, `swh:1:snp:be5e...`, `swh:1:snp:d15c...`, `swh:1:snp:92f8...`), and `research-timeline` fills the complementary need: a lightweight, archival-friendly format for the *process* of research, not just its artifacts.

# State of the Field

Existing ecosystem positions:

- **Notion/Obsidian/Jira** — cloud-dependent, proprietary formats, not CLI-scriptable, not research-specific.
- **DataVersionControl (DVC)** and **WandB** — designed for machine-learning experiment tracking; they track artifacts, metrics, and runs, not researcher-level project tasks across the full lifecycle (from literature review to reporting). They also impose a heavyweight installation and a model-specific data model.
- **BibTeX/Zotero ecosystems** — capture literature, not research progress.
- **Plain TODO lists in source** — no validation, no taxonomy, no export, not queryable.

`research-timeline` occupies the empty slot of a zero-dependency, human-readable, git-native lifecycle tracker: the progress file is YAML by default, lives next to the project's data, and the tool offers

`init`, `log`, `list`, `export`, and `validate` primitives with a minimal, learnable surface. Because the storage format is plain YAML, migration to other tools is trivial and no data is locked in.

# Software Design

The tool is a single Python package (Python ≥ 3.8) with a small API surface:

- `research_timeline.cli` — the `click`-based command-line interface with the commands `init`, `log`, `list`, `export`, and `validate`.
- Four lifecycle record fields: status (`pending`, `in_progress`, `completed`, `cancelled`), date, tags, and free-text notes.
- Storage: a single YAML document (`.timeline.yaml`) with a versioned schema, parseable by any YAML consumer — deliberately decoupled from any specific Python version or storage engine.
- Exporters for YAML, JSON, and Markdown, so consumers can render progress reports, status boards, or documentation snippets with no additional tooling.
- Validation performs structural integrity checks (required fields, allowed statuses, date format, list shape) and returns exit codes suitable for use in CI pipelines (e.g., check that a timeline is valid before a release).

The main architectural trade-off, deliberately made, is between richness and reliability: no database is used, no remote service is required, and the tool runs anywhere Python 3.8+ runs, including air-gapped systems and the researcher's laptop offline. This makes the format stable across decades of research practice without maintenance cost.

# Research Impact Statement

`research-timeline` has been used to track the N47Lab MatterMemory research program — a multi-year, multi-venue investigation of sub-planckian phase imprints as a dark-matter candidate validated through Phase-Anchored State Multiplexing (PASM) on IBM Quantum hardware. The timeline has been used to maintain version-controlled histories of the 13 completed QPU experiments, the 47-replicated dataset, and the associated publications, keeping a single authoritative view of research states across the entire analytical pipeline (literature, circuit design, QPU submission, FFT/MI analysis, replication, reporting). The pasm-experiments and N47Lab repositories, together with their Software Heritage snapshot(s) listed below, form the archival record in which the timeline is embedded as the process-level companion. It is adopted as the project-history standard in the author's repositories and is expected to be used in subsequent research outputs that reuse the open PASM workflow.

# AI Usage Disclosure

This project uses generative AI assistance during development and documentation. The specific tools used are: large language model assistants (GPT-4-class and DeepSeek-class models, June–August 2026) for drafting code scaffolding, documentation assistance, test scaffolding, and copy-editing of the paper. All AI-assisted outputs were reviewed, edited, validated, and the design decisions above (architecture, format, feature set) were made entirely by the human author. No opaque outputs were incorporated without verification by the author; the software is tested and validated under test-driven development.

# Installation

```bash
pip install -e .
# or from the archive:
pip install git+https://github.com/Strugiss/research-timeline.git
```

# Usage

```bash
research-timeline init
research-timeline log "Literature review" -s in_progress -t "lit,review"
research-timeline log "First draft done" -s completed -t writing -n "5000 words"
research-timeline list -s completed
research-timeline export -F md -o timeline.md
research-timeline validate
```

# Testing

```bash
pytest tests/ -v          # 7 tests passing
pytest --cov=research_timeline tests/   # with coverage
```

# License

MIT License — see `LICENSE`.

# References

- Baker, M. (2016) "1,500 scientists lift the lid on reproducibility", Nature 533, 452–454. doi:10.1038/533452a
- Zenodo archive: 10.5281/zenodo.21830143
- Software Heritage archive of this repository: `swh:1:snp:339028719a13fb1de3d99524c923e66cad65aeda`
- N47Lab research program (PASM / MatterMemory): https://github.com/Strugiss/N47Lab-QuantumResearch
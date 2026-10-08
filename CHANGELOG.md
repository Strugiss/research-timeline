# Changelog

All notable changes to research-timeline are documented here.
The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/) conventions.

## [v0.2.5] - 2026-10-08

### Changed
- Quality pass for the pyOpenSci review: `validate` and `log` now perform real
  JSON Schema (draft-07) validation via `jsonschema` (was basic manual checks);
  CI runs `ruff` and `mypy`; Python 3.9 dropped (end of life) — `>=3.10`;
  added `CITATION.cff` and a Citation section in the README; LaTeX/HTML
  exports escape special characters; timeline may be empty at `init`
  (schema `minItems: 0`; `orcid` may be null).

## [v0.2.4] - 2026-09-02

### Added
- `export --format csv` — machine-readable, spreadsheet-friendly export
- `export --format gantt` — publication-ready Gantt chart (LaTeX TikZ), with
  optional date ranges (`--end-date`)
- `list` filters: `--type`, `--tag`, `--since`, `--until`
- `stats` command: duration window, per-type and per-tag counts

### Changed
- Version 0.2.4; retired the uniqueness/empty-slot claim (RETTIFICA 01/09/2026):
  the landscape analysis now lists comparable existing tools
- README restructured (badges, terminal preview, quick start)
- AI Usage Disclosure wording finalized ("by the human author, with
  AI-assisted review for verification") — README, AI_POLICY.md, paper.md
- Docs CI fix: `[docs]` extra (mkdocs + material) required by the workflow
- README: AI usage disclosure section and PyPI install (pyOpenSci #338 request)

## [v0.2.3] - 2026-08-09

### Added
- MkDocs documentation site (Material theme): install, usage, file format,
  examples, AI disclosure, about — published on GitHub Pages
- Docs CI workflow; docs badge and link in README
- Citation with Zenodo DOI (10.5281/zenodo.21862618)
- Example timeline updated with real events: T3 (PRL submission
  es2026aug09_746) and T4 (pyOpenSci submission, issue #338)

### Changed
- Single-author-with-AI-assistance statement mirroring research-group role
  distribution (design, implementation, verification, drafting)

## [v0.2.2] - 2026-08-09

### Changed
- Honest AI disclosure wording: AI-assisted review, human responsibility —
  README, AI_POLICY.md, paper.md

## [v0.2.1] - 2026-08-09

PyPI release. Added pyOpenSci readiness files.

### Added
- Issue templates (bug report / feature request) and Pull Request template
- Contribution guidelines (`CONTRIBUTING.md`)
- CI pipeline (GitHub Actions: pytest + compile check on Python 3.9–3.12)
- README badges: CI status, Python versions, license, SWHID archive
- Reproducibility-focused `paper.md` (JOSS-format submission)
- `CODE_OF_CONDUCT.md` (Contributor Covenant 2.1)
- `AI_POLICY.md` — generative-AI usage policy (transparency + human oversight)
- README sections: AI Usage Disclosure, Related work (landscape analysis)
- Installation via PyPI (`pip install research-timeline`)

## [v0.2.0] - 2026-08-09

Restored the original full-featured research-timeline tool.

### Changed
- Complete rewrite of the CLI on **Typer + Pydantic + Rich** (was click/pyyaml)
- Storage format: **JSON** with typed schema (`schema/timeline.schema.json`), was YAML
- Event model: typed phases `T0`–`Tn`, `pivot`, `control`, `submission`, `publication`, `milestone`
- `metrics` and `evidence` (git commits, QPU job IDs, data/code links) attached to events
- Author record with `ai_role` disclosure (`cognitive_prosthesis`, `co_pilot`, `autonomous_agent`)
- Exports: LaTeX table, Markdown, standalone HTML, schema.org JSON-LD (was YAML/JSON/MD)
- Validation against the JSON schema with CI-friendly exit codes
- `__main__.py` entry point, `research-timeline` console script
- Real-world example timeline (`example/timeline.json`) with generated exports

### Fixed
- Event ID validation now accepts all typed phases (not only `T*`), rejecting invalid IDs
- `ai_role` is honored in `init` (was hardcoded)
- `data_links` and `code_links` are now stored in `evidence`
- Comma-separated lists (`--job-ids`, `--data-links`, `--code-links`) are split correctly

### Tests
- 14 pytest tests: CLI lifecycle (init/log/list/export/validate), typed ID acceptance,
  duplicate rejection, metrics/evidence persistence, all four export formats

## [v0.1.0] - 2026-08-06

Initial release (simplified click/pyyaml CLI).

### Added
- `init` — initialize a new timeline file
- `log` — append an entry with date, title, status, tags, notes
- `list` — list entries with filtering by status/tags and limiting
- `export` — YAML/JSON/Markdown export
- `validate` — structural and content validation with CI-friendly exit codes
- Zero-dependency CLI (click, pyyaml, rich)
- 7 pytest tests, MIT license, Zenodo DOI (10.5281/zenodo.21830143)
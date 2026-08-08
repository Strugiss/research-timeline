# Changelog

All notable changes to research-timeline are documented here.
The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/) conventions.

## [Unreleased]

### Added
- Issue templates (bug report / feature request) and Pull Request template
- Contribution guidelines (`CONTRIBUTING.md`)
- CI pipeline (GitHub Actions: pytest + compile check on Python 3.9–3.12)
- README badges: CI status, Python versions, license, SWHID archive
- Reproducibility-focused `paper.md` (JOSS-format submission)

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
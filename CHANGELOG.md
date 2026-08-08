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

## [v0.1.0] - 2026-08-06

Initial release.

### Added
- `init` — initialize a new timeline file
- `log` — append an entry with date, title, status, tags, notes
- `list` — list entries with filtering by status/tags and limiting
- `export` — YAML/JSON/Markdown export
- `validate` — structural and content validation with CI-friendly exit codes
- Zero-dependency CLI (click, pyyaml, rich)
- 7 pytest tests, MIT license, Zenodo DOI (10.5281/zenodo.21830143)
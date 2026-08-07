---
title: "research-timeline: A CLI tool for tracking research progress"
authors:
  - name: Alessandro Tulli
    affiliation: "N47Lab"
    orcid: "0009-0008-9201-6080"
date: 2026-08-07
version: "v0.1.0"
doi: "10.5281/zenodo.21830143"
repository: "https://github.com/Strugiss/research-timeline"
---

# Summary

A simple command-line tool for tracking research progress — designed for independent researchers.

# Statement of Need

Independent researchers lack lightweight, portable tools for tracking research progress without institutional infrastructure. Existing tools (Notion, Obsidian, Jira) are either cloud-dependent, complex, or not designed for research workflows. `research-timeline` provides a zero-dependency CLI with human-readable YAML storage that integrates naturally with git workflows.

# Functionality

- **init** — initialize timeline file
- **log** — add entry (title, status, tags, notes, date)
- **list** — show entries (filter by status/tag, limit)
- **export** — YAML, JSON, Markdown
- **validate** — check required fields, valid statuses

Status values: `pending`, `in_progress`, `completed`, `cancelled`.

# Installation

```bash
pip install -e .
# or: pip install git+https://github.com/Strugiss/research-timeline.git
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
pytest tests/ -v
# 7 passed
```

# License

MIT License — see LICENSE file.

# References

- Zenodo: 10.5281/zenodo.21830143
- GitHub: https://github.com/Strugiss/research-timeline
- N47Lab / MatterMemory project
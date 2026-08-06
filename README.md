# Research Timeline

A simple CLI tool for tracking research progress - designed for independent researchers.

## Features

- **Log entries** with date, title, status, tags, notes
- **List/filter** by status or tags
- **Export** to YAML, JSON, or Markdown
- **Validate** timeline integrity
- **Simple YAML storage** - human readable, git-friendly

## Installation

```bash
pip install -e .
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

- `pending` - not started
- `in_progress` - actively working
- `completed` - done
- `cancelled` - abandoned

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

## License

MIT
# Usage

All commands take a `--file`/`-f` option to select the timeline file (default: `.research-timeline.json` in the current directory).

## `init` — create a new timeline

```bash
research-timeline init \
  --name "PASM DTC Discovery" \
  --desc "Observation of Classical Prethermal DTC on IBM Heron" \
  --domain quantum \
  --author "N47Lab" \
  --affiliation independent \
  --ai-role cognitive_prosthesis \
  --output timeline.json
```

| Option | Required | Description |
|--------|----------|-------------|
| `--name`, `-n` | yes | Project name |
| `--desc`, `-d` | yes | Project description |
| `--domain` | no | Research domain (default `quantum`) |
| `--author`, `-a` | yes | Author name |
| `--affiliation` | no | Affiliation (default `independent`) |
| `--orcid` | no | ORCID URL |
| `--background` | no | Academic background (default `without academic degrees`) |
| `--ai-role` | no | AI role: `cognitive_prosthesis`, `co_pilot`, `autonomous_agent` (default `cognitive_prosthesis`) |
| `--output`, `-o` | no | Output file (default `.research-timeline.json`) |

## `log` — add a typed event

```bash
research-timeline log T1 \
  --type T1 \
  --date 2026-07-31 \
  --desc "First commit: 14 QPU experiments, Z>50sigma" \
  --z-combined 50.0 \
  --git-commit c3ddc4a \
  --job-ids marrakesh-pasm-1 \
  --tags commit,qpu \
  --file timeline.json
```

**Valid event IDs:** `T0`, `T1`, …, `Tn`, `pivot`, `control`, `submission`, `publication`, `milestone`.
Duplicate IDs are rejected.

| Option | Required | Description |
|--------|----------|-------------|
| `event_id` | yes (positional) | Event ID, must match a valid typed phase |
| `--type` | yes | Event type (free text, usually same as ID) |
| `--date` | no | Event date `YYYY-MM-DD` (default: today) |
| `--desc` | yes | Event description |
| `--tags` | no | Comma-separated tags |
| `--z-score` | no | Z-score metric |
| `--shots` | no | Shots metric |
| `--backend` | no | Quantum backend metric |
| `--job-ids` | no | Comma-separated IBM Quantum job IDs (evidence) |
| `--z-combined` | no | Combined Z-score metric |
| `--git-commit` | no | Git commit hash (evidence) |
| `--data-links` | no | Comma-separated data repository links (evidence) |
| `--code-links` | no | Comma-separated code repository links (evidence) |
| `--file`, `-f` | no | Timeline file (default `.research-timeline.json`) |

## `list` — display events

```bash
research-timeline list --metrics --file timeline.json
```

| Option | Description |
|--------|-------------|
| `--metrics`, `-m` | Also show metrics |
| `--file`, `-f` | Timeline file |

## `export` — export to papers/reports/web

```bash
research-timeline export --format latex -o timeline.tex --file timeline.json
research-timeline export --format markdown -o timeline.md --file timeline.json
research-timeline export --format html -o timeline.html --file timeline.json
research-timeline export --format jsonld -o timeline.jsonld --file timeline.json
```

| Option | Description |
|--------|-------------|
| `--format` | `latex`, `markdown`, `html`, `jsonld` (default `latex`) |
| `--output`, `-o` | Output file (default: print to stdout) |
| `--file`, `-f` | Timeline file |

- **LaTeX** — a `table` environment ready for manuscripts and reports
- **Markdown** — a portable table for READMEs
- **HTML** — a standalone interactive widget (Chart.js, no build step)
- **JSON-LD** — schema.org `ResearchProject` metadata for archives and repositories

## `validate` — check a timeline against the schema

```bash
research-timeline validate --file timeline.json
```

Prints `[OK] Timeline is valid!` on success, or a list of errors with exit code 1 (CI-friendly).

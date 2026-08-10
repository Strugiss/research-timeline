# File Format

A timeline is a **single JSON document** — human readable, diff-friendly, git-native, zero lock-in.

## Structure

```json
{
  "project": {
    "name": "PASM DTC Discovery",
    "description": "Observation of Classical Prethermal DTC on IBM Heron",
    "domain": "quantum"
  },
  "author": {
    "name": "N47Lab",
    "affiliation": "independent",
    "orcid": null,
    "background": "without academic degrees",
    "ai_role": "cognitive_prosthesis"
  },
  "events": [
    {
      "id": "T1",
      "type": "T1",
      "date": "2026-07-31",
      "description": "First commit: 14 QPU experiments, Z>50sigma",
      "tags": ["commit", "qpu", "baseline"],
      "metrics": {
        "z_score_combined": 50.0,
        "experiments": 14
      },
      "evidence": {
        "git_commit": "c3ddc4a",
        "job_ids": ["marrakesh-pasm-1"]
      }
    }
  ],
  "created_at": "2026-06-06",
  "updated_at": "2026-08-10",
  "version": "1.0"
}
```

## Sections

### `project` (required)

| Field | Description |
|-------|-------------|
| `name` | Project name |
| `description` | Brief project description |
| `domain` | Research domain (quantum, biology, ml, physics, chemistry, materials, computer_science, other) |

### `author` (required)

| Field | Description |
|-------|-------------|
| `name` | Author name |
| `affiliation` | Institutional affiliation or `independent` |
| `orcid` | ORCID identifier (URI) or `null` |
| `background` | Academic background / credentials |
| `ai_role` | Role of AI: `cognitive_prosthesis`, `co_pilot`, `autonomous_agent` |

### `events` (required, at least 1)

Each event has:

| Field | Required | Description |
|-------|----------|-------------|
| `id` | yes | `T0`–`Tn`, `pivot`, `control`, `submission`, `publication`, `milestone` — must be unique |
| `type` | yes | Event type (free text, usually the same as the ID) |
| `date` | yes | ISO 8601 date (`YYYY-MM-DD`) |
| `description` | yes | Human-readable description |
| `tags` | no | Array of category strings |
| `metrics` | no | Free-form key/value pairs with quantitative results (z-scores, shots, MI, backend, …) |
| `evidence` | no | Structured support: `git_commit`, `job_ids` (array), `data_links` (array), `code_links` (array), plus any additional fields |

## Validation

The full contract is defined in `schema/timeline.schema.json` (JSON Schema draft-07).

Validate any timeline against the schema at the CLI:

```bash
research-timeline validate --file timeline.json
```

or in CI:

```bash
python -c "import json,jsonschema; json.load(open('timeline.json',encoding='utf-8'))"
```

The CLI also rejects invalid or duplicate event IDs at input time.

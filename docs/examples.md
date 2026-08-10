# Examples

## Real-world timeline: PASM DTC Discovery

The `example/timeline.json` in the repository is a **real, complete timeline** from the N47Lab research program (sub-planckian phase-imprint dark-matter candidates explored with Phase-Anchored State Multiplexing on IBM Quantum hardware).

It records the full process, from the first AI interaction to journal submissions:

| Event | Date | What happened |
|-------|------|---------------|
| `T0` | 2026-06-06 | First AI interaction: setup, theory, protocol design |
| `T1` | 2026-07-31 | First commit: 14 QPU experiments, combined Z > 50σ |
| `T2` | 2026-08-04 | Replica 10×: Z = 39.6σ, shared MI 0.063 ± 0.005 |
| `pivot` | 2026-08-04 | Switch to φ-decoupling scan: MI modulated by φ, peak at π |
| `control` | 2026-08-05 | Witness control: MI = 0.00013 (zero), QST/discord cross-check |
| `milestone` | 2026-08-06 | Scaling study: MI peaks at 3 qubits (0.159), distance-independent |
| `submission` | 2026-08-07 | Submitted to JOSS |
| `T3` | 2026-08-09 | Manuscript submitted to Physical Review Letters (es2026aug09_746) |
| `T4` | 2026-08-10 | research-timeline submitted for pyOpenSci peer review (issue #338) |

Every event carries its metrics and evidence (git commits, QPU job IDs, DOIs).

## Generated exports

The repository also ships the generated exports of this timeline in `example/`:

- `timeline_output.tex` — LaTeX table, ready for manuscripts
- `timeline_output.md` — Markdown table
- `timeline_output.html` — standalone interactive widget
- `timeline_output.jsonld` — schema.org metadata (ResearchProject)

## Minimal walkthrough

```bash
# 1. Init a timeline for a new project
research-timeline init \
  --name "My Project" --desc "My research" --author "Jane Doe" \
  --output timeline.json

# 2. Log the first phase
research-timeline log T0 --type T0 --desc "Literature review" \
  --tags setup --file timeline.json

# 3. Log a result with metrics and evidence
research-timeline log T1 --type T1 --desc "First dataset collected" \
  --z-score 5.3 --git-commit a1b2c3d \
  --data-links https://zenodo.org/record/example \
  --file timeline.json

# 4. Inspect and export
research-timeline list --metrics --file timeline.json
research-timeline export --format latex -o timeline.tex --file timeline.json
research-timeline export --format jsonld -o timeline.jsonld --file timeline.json

# 5. Validate before committing
research-timeline validate --file timeline.json
```

A typical workflow: keep `timeline.json` in your repository, log an event at each milestone, validate in CI, and export to LaTeX when writing the paper.

# research-timeline

Track, validate, and export research timelines — from first AI interaction to scientific discovery.

`research-timeline` documents the **process** of research, not just its artifacts: every milestone of a project (the first AI interaction that shaped the protocol, the first QPU commit with its evidence, pivots, controls, submissions, publications) is recorded in a single versioned JSON file with typed events, quantitative metrics, and supporting evidence.

## Features

- **Typed events** — `T0`, `T1`…`Tn`, `pivot`, `control`, `submission`, `publication`, `milestone`
- **Metrics** — attach any quantitative result (z-scores, shots, backend, MI, …) to an event
- **Evidence** — git commits, IBM Quantum job IDs, data links, code links
- **AI-role disclosure** — each timeline declares how AI was used (`cognitive_prosthesis`, `co_pilot`, `autonomous_agent`)
- **Exports** — LaTeX table (papers/reports), Markdown, standalone HTML, schema.org JSON-LD
- **Validate** — structural checks with CI-friendly exit codes
- **Simple JSON storage** — human readable, diff-friendly, git-native, zero lock-in

## Quick start

```bash
pip install research-timeline
research-timeline init --name "My Project" --desc "A project" --author "Jane Doe"
research-timeline log T1 --type T1 --desc "First result" --z-combined 50.0
research-timeline list
```

See [Usage](usage.md) for the full command reference, and [Examples](examples.md) for a real-world timeline (the PASM DTC Discovery project on IBM Quantum hardware).

## License

MIT — see [LICENSE](https://github.com/Strugiss/research-timeline/blob/main/LICENSE).

# About

## Motivation

The reproducibility literature shows that **process information is exactly what gets lost** when results are shared. Standard task trackers and experiment trackers do not model research phases; nothing records the role of generative AI in the workflow in a machine-readable way.

In the era of AI-assisted research, there is a need for a citable, versionable record that:

1. discloses the role AI played (`cognitive_prosthesis`, `co_pilot`, `autonomous_agent`), and
2. anchors each step to verifiable evidence — commits, QPU job IDs, data/code links

so that "how the research happened" is as reproducible as the results themselves.

`research-timeline` provides that record with a minimal, CI-friendly, schema-validated tool.

## Design philosophy

- **Simplicity over power** — no database, no cloud, no lock-in
- **Git-native** — a single JSON file that diffs cleanly and versionizes with your code
- **Offline-first** — works on a plane, in a lab, or in a notebook without network
- **Decades-durable** — plain JSON readable by any parser, archived via Zenodo and Software Heritage

## How it differs from other tools

- **Notes/task tools (Notion, Obsidian, Logseq, Trello)** — no typed research phases, no JSON schema, no CI validation, cloud-bound
- **Experiment trackers (Weights & Biases, MLflow, DVC)** — track model runs and artifacts, not researcher-level process events, and no paper-oriented exports
- **Notebooks (Jupyter, Quarto)** — rich narrative but unstructured, no schema enforcement, no machine-readable JSON-LD export
- **Lab notebooks (ELN, Code Ocean)** — heavyweight, instrument-locked, or cloud-bound

`research-timeline` fills a specific slot: a **provenance instrument for the research process**. RETTIFICA (01/09/2026): an earlier claim of uniqueness was retracted - timeline visual tools exist (timeline-fishbone-generator, timeline-maker, SubThesis Timeline Generator, Research-Timeline-Planner, The Timeline Project); this tool differs by design, not by existence.

## Credits & provenance

- **Author**: Alessandro Tulli (independent researcher, N47Lab)
- **Used by**: the PASM DTC Discovery program on IBM Quantum hardware (see [Examples](examples.md))
- **Archived**: [Zenodo](https://doi.org/10.5281/zenodo.21855315) · [Software Heritage](https://archive.softwareheritage.org/swh:1:snp:62a2f748e52113016cf291c4b8c944e86c6848bf/)
- **Peer review**: [pyOpenSci submission #338](https://github.com/pyOpenSci/software-submission/issues/338)

## License

MIT — see [LICENSE](https://github.com/Strugiss/research-timeline/blob/main/LICENSE).

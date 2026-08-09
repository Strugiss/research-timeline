# Contributing to research-timeline

Thanks for considering contributing! This project follows a simple, open workflow.

## Development setup

```bash
git clone https://github.com/Strugiss/research-timeline.git
cd research-timeline
python -m venv .venv
.venv\Scripts\activate  # Windows
# source .venv/bin/activate  # Linux/macOS
pip install -e ".[dev]"
```

## Running tests

```bash
pytest tests/ -v
```

## Making changes

1. Open an issue first for non-trivial changes (bug, feature, design).
2. Create a branch: `git checkout -b feature/your-change`.
3. Add tests for any new behavior; keep the existing suite green.
4. Run `pytest tests/ -v` and `python -m compileall src/`.
5. Update `CHANGELOG.md` under "Unreleased".
6. Commit with a concise message; open a Pull Request describing the change.

## Conventions

- Follow PEP 8 / `ruff` defaults; type annotations are welcome.
- Storage format moves only via explicit version bumps in the YAML schema.
- Keep the dependency footprint minimal: no new runtime dependencies without discussion.
- All user-visible output is in English; project docs in Italian may accompany it.

## Code of conduct

Be respectful. Harassment of any kind will not be tolerated in issue or PR discussions. See [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md) and [AI_POLICY.md](AI_POLICY.md) for the full policies.

## Governance

The project is currently maintained solely by the author. Forks, issues, and PRs are welcome. If the project gains active contributors, a simple maintainers model will be adopted (see CHANGELOG for decisions).
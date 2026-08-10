# AI Disclosure

`research-timeline` was itself developed with the assistance of generative AI tools (interactive AI coding assistants with agentic workflows).

## How AI was used

- Initial code scaffolding
- The test suite
- Documentation drafting (June–August 2026)

## How the human kept control

- **All AI-assisted output was reviewed by the human author**, with AI-assisted review for verification
- **Design decisions** (schema, event types, export contracts, `ai_role` semantics) and **final acceptance of every change** were made by the human author
- Algorithmic behavior is covered by the test suite in `tests/` and by CI

## The `ai_role` field

The tool itself records the role of AI in any research process it documents:

| Value | Meaning |
|-------|---------|
| `cognitive_prosthesis` | AI extends the human's cognitive capabilities; the human makes the decisions |
| `co_pilot` | AI proposes and the human selects, in an interactive loop |
| `autonomous_agent` | AI operates with a high degree of autonomy |

This mirrors the distribution of roles in a research group (design, implementation, verification, drafting), with the human author bearing **full responsibility** for the final result.

## Full policy

See [AI_POLICY.md](https://github.com/Strugiss/research-timeline/blob/main/AI_POLICY.md) in the repository for the complete generative-AI usage policy.

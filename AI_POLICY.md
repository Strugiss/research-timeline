# AI Policy

*research-timeline* — effective August 2026

## Scope

This policy governs the use of generative AI tools in the development and
maintenance of this package.

## Transparency

Generative AI tools (interactive AI coding assistants with agentic workflows)
were used during development, covering:

- Initial code scaffolding of the CLI and data models;
- The test suite;
- Documentation drafting (README, docstrings, exports);
- This policy document itself was drafted with AI assistance.

## Human oversight

All AI-assisted output is reviewed by the human author, with AI-assisted
review for verification, before it is committed. The human author is
responsible for:

- All design decisions (schema, event types, export contracts, `ai_role`
  semantics, CLI surface);
- Review and acceptance of every AI-suggested change;
- Correctness of the implementation, verified through the test suite and CI.

No AI-generated code is merged without human review, understanding, and
explicit acceptance.
## Use of AI in this repository's artifacts

- **Code**: AI-generated scaffolding and suggestions, human-reviewed and
  tested. The current implementation is understood by the human author.
- **Documentation**: AI-drafted text, human-edited for accuracy.
- **Communications**: issue and pull request discussions are written by the
  human author. AI may be used for translation and grammar correction only.

## Reporting

This policy is reviewed whenever development practices change significantly.
Questions about this policy can be raised via the repository issue tracker.

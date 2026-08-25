# SpecKit Grill With Docs (base)

This skill thoroughly clarifies a Spec Kit feature specification and synchronizes settled project-wide terminology, domain knowledge, and design decisions to ordinary Markdown documents without depending on Serena.

## Default document layout

Unless the target project explicitly designates another canonical location, use:

```text
docs/domain_knowledge/
├── CONTEXT.md
├── <kebab-case-domain-topic>.md
└── adr/
    └── 0001-<kebab-case-decision>.md
```

When the project designates another canonical knowledge root, use its existing context-entry and ADR conventions; otherwise place the entry point at `<knowledge-root>/CONTEXT.md` and ADRs under `<knowledge-root>/adr/`.

- `CONTEXT.md` is the knowledge-base entry point. It concisely holds project-specific canonical terms, concept boundaries, and synonyms to avoid without mixing in implementation details or feature specifications. Its headings follow the target project's documentation language and conventions.
- Create a separate Markdown document only when several boundaries, invariants, or business rules cannot be represented accurately in one or two sentences. When in doubt, keep the content in `CONTEXT.md`.
- Link every topic document from `CONTEXT.md` with a relative link.
- Record in `adr/` only decisions that are costly to reverse, surprising without context, and selected from real alternatives.
- Keep feature-specific requirements in `spec.md` and cross-feature canonical knowledge in this directory.

This separation draws on the concise glossary and just-in-time ADR approach in Matt Pocock's [domain-modeling](https://github.com/mattpocock/skills/tree/main/skills/engineering/domain-modeling), while standardizing the storage location as `docs/domain_knowledge/`.

## Dependencies

- macOS or Linux
- Bash
- A Spec Kit project containing `.specify/`
- The sibling `speckit-grill-me` skill

Serena, Serena MCP, and `.serena/` are not required.

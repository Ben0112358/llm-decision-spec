# Documentation index

Agent-optimized, human-readable reference for `llm-decision-spec`. Code and tests are the source of truth for APIs; these docs capture architecture, domain rules, and conventions that are easy to get wrong.

## Where to start

| If you are… | Read |
|-------------|------|
| New to the codebase | [overview.md](overview.md) → [architecture.md](architecture.md) |
| Changing evaluation behavior | [architecture.md](architecture.md) + [domain.md](domain.md) |
| Adding an Expr, Operator, or Reducer | [conventions.md](conventions.md) + matching package under `tests/` |
| Running checks or CI | [development.md](development.md) |
| Understanding a past design choice | [decisions/](decisions/) |

## Files

| File | Contents |
|------|----------|
| [overview.md](overview.md) | Project intent, non-goals, current status |
| [architecture.md](architecture.md) | Expr → Operator → Reducer pipeline, package layout |
| [domain.md](domain.md) | Events, Context, missing (`None`), temporal model |
| [conventions.md](conventions.md) | API patterns, extension checklist, test layout |
| [development.md](development.md) | Local setup, commands, CI workflows |
| [decisions/](decisions/) | Architecture decision records (ADRs) |

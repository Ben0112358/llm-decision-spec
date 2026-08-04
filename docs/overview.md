# Overview

`llm-decision-spec` is a work-in-progress library for defining event-based features as a composable AST.

## What it is

A feature intermediate representation built from three layers:

1. **Expr** — project a value from one event
2. **Operator** — select events from a `Context`
3. **Reducer** — aggregate over selected events into a scalar

The same AST is intended to work for offline batch evaluation and online serving, so features defined once can be executed in either environment without rewriting logic.

## Why it exists

The project serves two goals:

- **Knowledge base** — encode decision logic and feature definitions in a structured, inspectable form
- **Feature generation layer** — provide a target representation for LLM-assisted feature authoring

See [architecture.md](architecture.md) for the pipeline and package layout.

## Non-goals (current)

- Execution engine or orchestration beyond in-memory evaluation
- Persistence, streaming, or distributed computation
- SQL / codegen / serialization (may come later)
- Schema enforcement on event dicts

## Status

Active development. Core Expr, Operator, and Reducer paths are implemented and tested. Some modules are stubs.

## Current gaps

| Item | Location | Notes |
|------|----------|-------|
| `NullIf` | `expressions/control.py` | Stub (`pass`) |
| Relation Operators | `operators/relation.py` | Not implemented |

Do not build features that depend on these until they are implemented.

## See also

- [README.md](README.md) — documentation index
- [architecture.md](architecture.md) — start here for implementation work
- [development.md](development.md) — local setup

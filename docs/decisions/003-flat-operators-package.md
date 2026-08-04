# ADR 003: Flat operators package with core and util

## Context

Operators, selection helpers, validation, and runtime types were split across `filters/`, `execution/`, `operators/predicate.py`, and `operators/_validate.py`. The layout did not mirror the mental model (Expr → Operator → Reducer) and made imports harder to navigate.

## Decision

Restructure into:

- `core/` — `Context`, `EvaluationResult`
- `operators/` — flat; all selection Operators (formerly under `filters/`)
- `util/` — `selection.py` (predicate skeleton), `validate.py` (`_require_operator`)
- Remove `execution/`, `filters/`, and the old `operators/predicate.py` / `operators/_validate.py`

Tests mirror the same first-level package names under `tests/`.

## Consequences

- Package names match layer responsibilities.
- One import path for Operators (`llm_decision_spec.operators.*`).
- Move-only refactor; no evaluation logic changed.

# ADR 002: None as the sole missing representation

## Context

Events are untyped dicts. Fields may be absent, comparisons may involve missing operands, and reducers should skip incomplete rows. We need one consistent rule across Expr, Operator, and Reducer layers.

## Decision

Missing values are represented as `None` in Python. There is no separate sentinel (no `MISSING` enum, no `Optional` wrapper type). Each layer handles `None` explicitly:

- Expr: propagate `None` through arithmetic and string expressions
- Operator: skip events when predicate operands are missing
- Reducer: exclude missing values via `valid_value`

`Has(Field)` tests key existence in the event dict, not whether the stored value is `None`.

## Consequences

- Simple mental model aligned with Python idioms.
- Callers must not use `None` as a legitimate business value if they rely on missing semantics.
- Predicate Operators never raise on missing data; they silently skip.

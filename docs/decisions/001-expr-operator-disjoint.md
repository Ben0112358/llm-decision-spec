# ADR 001: Expr and Operator are disjoint AST domains

## Context

Features combine value projection (read a field, add two numbers) with event selection (filter by amount, date, membership). These are different responsibilities with different evaluation signatures: per-event vs over a `Context`.

## Decision

`Expr` and `Operator` are separate class hierarchies with no shared ABC. Construction-time guards (`_require_expr`, `_require_operator`) prevent mixing them. Selection is composed with logical Operators (`And`, `Or`, `Not`, `Difference`), not a `BoolExpr` or `Where` layer.

## Consequences

- Clear layer boundaries: Expr projects, Operator selects, Reducer aggregates.
- Slightly more verbose trees than a unified AST, but each node type has one job.
- Type errors surface at construction, not at evaluation time.

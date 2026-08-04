# Domain model

Vocabulary and semantics for events, missing values, and time.

## Constraints

- An **event** is a `dict` row. Identity is defined by `Context.event_key_fn`, not by object identity.
- **Missing** is represented only as `None`. There is no separate sentinel type.
- `Has(Field)` tests **key existence** (`name in event`), not whether the value is non-null.
- Temporal Operators that compare against an `Expr` **skip** events where that Expr evaluates to `None`.

## Events and Context

Each event is an untyped `dict`. The library does not enforce a schema; callers supply field names via `Field("name")` and populate `Context` accordingly.

`Context` holds:

- the full event universe (`events`)
- how to identify an event (`event_key_fn`)
- how to read an event's timestamp (`event_datetime_fn`)
- the evaluation reference time (`context_datetime`)

Logical Operators (`And`, `Or`, `Not`, `Difference`) combine results by event key. Two dicts with the same key are treated as the same event even if they are different objects.

### Test fixture

[`tests/conftest.py`](../tests/conftest.py) defines a standard fixture:

- 3 events with `id`, `amount`, `currency`, `merchant`, `datetime`
- `event_key_fn = lambda e: e["id"]`
- `context_datetime = 2026-01-04 11:00:00`

Use this fixture when reasoning about temporal or aggregation behavior in tests.

## Missing (`None`) propagation

Rules are defined in [`expressions/evaluate.py`](../src/llm_decision_spec/expressions/evaluate.py).

| Layer | When a value is `None` |
|-------|----------------------|
| Expr (arithmetic, string) | Propagate `None` through the expression |
| Operator (binary predicate) | Skip the event (do not include in `EvaluationResult.data`) |
| Operator (`Has` / `Missing`) | Key presence only; value is irrelevant |
| Reducer | Exclude via `valid_value`; missing values do not contribute to aggregation |

`predicate_values(left, right, event)` returns `None` if either side is missing, which causes predicate Operators to skip that event without raising.

Reducers use `valid_value(expr, event)` which returns `None` when the Expr evaluates to missing, so aggregates like `Sum` ignore those rows.

## Temporal Operators

Implemented in [`operators/temporal.py`](../src/llm_decision_spec/operators/temporal.py).

### Absolute (compare event time to an Expr)

`Before`, `StrictlyBefore`, `After`, `StrictlyAfter` compare `context.datetime(event)` against the value of a right-hand `Expr`. If the Expr is missing for an event, that event is skipped.

### Relative (compare event time to `context_datetime`)

`EventWithinXDays`, `EventBeyondXDays`, and `EventFromXDaysBackToYDaysBack` use day deltas from `context.context_datetime`. These Operators do not take an `Expr` for the reference time; the reference is always `context_datetime`.

`EventFromXDaysBackToYDaysBack(x, y)` requires `x >= y` or construction raises `ValueError`.

## Presence Operators

`Has(Field)` and `Missing(Field)` in [`operators/presence.py`](../src/llm_decision_spec/operators/presence.py) filter on whether a key exists in the event dict. They do not evaluate the field value.

## See also

- [architecture.md](architecture.md) — pipeline and package layout
- [decisions/002-none-as-missing.md](decisions/002-none-as-missing.md)
- [conventions.md](conventions.md) — canonical constructors (`Field`, `Const`)

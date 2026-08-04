# Conventions

Patterns for extending the codebase without breaking layer boundaries.

## Constraints

- Use `Field("name")` and `Const(value)` in constructors. DO NOT pass raw strings where an `Expr` is expected.
- `In` / `NotIn` require the RHS to be `Const` wrapping a `set` or `frozenset`.
- `Regex` requires the pattern to be `Const` wrapping a `str`.
- New **value-driven Operators** (compare or filter by Expr values) MUST use helpers in [`util/selection.py`](../src/llm_decision_spec/util/selection.py). Do not duplicate the event loop.
- New **logical Operators** MUST validate children via [`util/validate.py`](../src/llm_decision_spec/util/validate.py).
- New **Expr** types MUST reject `Operator` children via `_require_expr` in [`expressions/base.py`](../src/llm_decision_spec/expressions/base.py).
- Tests mirror `src/llm_decision_spec/` at the first directory level. Shared helpers go in `tests/utils/`, not in a mirrored package.

## Extension checklist

### Add an Expr

1. Subclass `Expr` (or `BinaryExpr` / `UnaryExpr`) in the appropriate module under `expressions/`.
2. Implement `eval(self, event: dict) -> Any | None`.
3. Use `_require_expr` for child nodes in `__init__`.
4. Add tests under `tests/expressions/`.
5. Export from `expressions/__init__.py` if part of the public surface.

### Add a value-driven Operator

1. Subclass `Operator` in the appropriate module under `operators/`.
2. Call a helper from `util/selection.py`:
   - `filter_events_by_predicate` — unary or binary value match
   - `filter_events_by_str_binary` — both sides must be `str`
   - `filter_events_by_event_datetime` / `filter_events_by_context_datetime` — temporal
3. Add tests under `tests/operators/`.
4. DO NOT import from reducers or put aggregation logic in the Operator.

### Add a logical Operator

1. Subclass `Operator` in `operators/logical.py` (or extend that module's patterns).
2. Validate children with `_require_operator` / `_require_operators`.
3. Combine child `EvaluationResult.data` using `context.key(event)` for set operations.
4. Add tests under `tests/operators/`.

### Add a Reducer

1. Subclass `Reducer` in the appropriate module under `reducers/`.
2. Accept an `Expr` in `__init__`; validate with `_require_expr`.
3. In `evaluate(operator, context)`, call `operator.evaluate(context).data` and aggregate using `valid_value` where appropriate.
4. Add tests under `tests/reducers/`.

## Test layout

| Source package | Test directory |
|----------------|----------------|
| `expressions/` | `tests/expressions/` |
| `operators/` | `tests/operators/` |
| `util/` | `tests/util/` |
| `reducers/` | `tests/reducers/` |
| `core/` | `tests/core/` (placeholder; `Context` exercised via root `conftest.py`) |
| cross-layer smoke | `tests/test_feature_pipeline.py` (repo root) |
| shared helpers | `tests/utils/` |

When adding a feature, place tests in the directory that mirrors the package you changed. Follow existing assertion helpers in `tests/utils/assertions.py` and `tests/utils/operators.py` where applicable.

## API patterns

| Construct | Pattern |
|-----------|---------|
| Field access | `Field("amount")` |
| Literal | `Const(50)`, `Const("SEK")`, `Const(frozenset({...}))` |
| Comparison | `Gt(Field("x"), Const(1))` |
| Membership | `In(Field("currency"), Const(frozenset({"USD"})))` |
| Composition | `And(op_a, op_b)` — both children are Operators |
| Aggregation | `Sum(Field("amount")).evaluate(operator, context)` |

## See also

- [architecture.md](architecture.md) — layer responsibilities
- [domain.md](domain.md) — `None` and temporal semantics
- [development.md](development.md) — running tests locally

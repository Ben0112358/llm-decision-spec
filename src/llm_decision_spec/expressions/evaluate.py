"""Evaluation helpers.

None means missing (evaluated absence). Propagation rules:
- arithmetic/string Expr: propagate None
- predicate operators: skip event on None (via predicate_values)
- reducers: valid_value excludes None
"""

from typing import Any

from llm_decision_spec.expressions.base import Expr


def eval_expr(expr: Expr, event: dict) -> Any | None:
    return expr.eval(event)


def is_missing(value: Any) -> bool:
    return value is None


def valid_value(expr: Expr, event: dict) -> Any | None:
    v = eval_expr(expr, event)
    return None if is_missing(v) else v


def predicate_values(
    left: Expr, right: Expr, event: dict
) -> tuple[Any, Any] | None:
    lv = eval_expr(left, event)
    rv = eval_expr(right, event)
    if is_missing(lv) or is_missing(rv):
        return None
    return lv, rv

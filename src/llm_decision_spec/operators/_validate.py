from __future__ import annotations

from typing import Any

from llm_decision_spec.expressions.base import Expr
from llm_decision_spec.operators.base import Operator


def _require_operator(node: Any, name: str) -> Operator:
    if isinstance(node, Expr):
        raise TypeError(f"{name} must be Operator, got Expr")
    if not isinstance(node, Operator):
        raise TypeError(f"{name} must be Operator, got {type(node)}")
    return node


def _require_operators(
    children: tuple[Any, ...], op_name: str
) -> tuple[Operator, ...]:
    return tuple(_require_operator(c, f"{op_name} child") for c in children)

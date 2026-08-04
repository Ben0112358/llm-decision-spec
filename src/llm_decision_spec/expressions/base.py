from abc import ABC, abstractmethod
from typing import Any


class Expr(ABC):
    @abstractmethod
    def eval(self, event: dict) -> Any | None:
        """Return a value for one event, or None if missing."""
        raise NotImplementedError


def _require_expr(node: Any, name: str) -> Expr:
    from llm_decision_spec.operators.base import Operator

    if isinstance(node, Operator):
        raise TypeError(f"{name} must be Expr, got Operator")
    if not isinstance(node, Expr):
        raise TypeError(f"{name} must be Expr, got {type(node)}")
    return node


class Const(Expr):
    def __init__(self, value: Any):
        self.value = value

    def eval(self, event: dict) -> Any:
        return self.value


class BinaryExpr(Expr):
    def __init__(self, left: Expr, right: Expr):
        self.left = _require_expr(left, "left")
        self.right = _require_expr(right, "right")


class UnaryExpr(Expr):
    def __init__(self, operand: Expr):
        self.operand = _require_expr(operand, "operand")

from llm_decision_spec.expressions.base import Expr, UnaryExpr, _require_expr
from llm_decision_spec.expressions.evaluate import is_missing


def _require_str(v, op_name: str) -> str:
    if not isinstance(v, str):
        raise TypeError(f"{op_name} requires str, got {type(v)}")
    return v


class Lower(UnaryExpr):
    def eval(self, event: dict):
        v = self.operand.eval(event)
        if is_missing(v):
            return None
        return _require_str(v, "Lower").lower()


class Upper(UnaryExpr):
    def eval(self, event: dict):
        v = self.operand.eval(event)
        if is_missing(v):
            return None
        return _require_str(v, "Upper").upper()


class Length(UnaryExpr):
    def eval(self, event: dict):
        v = self.operand.eval(event)
        if is_missing(v):
            return None
        return len(_require_str(v, "Length"))


class Concat(Expr):
    def __init__(self, *parts: Expr):
        if not parts:
            raise ValueError("Concat requires at least one part")
        self.parts = tuple(_require_expr(p, "part") for p in parts)

    def eval(self, event: dict):
        values = []
        for part in self.parts:
            v = part.eval(event)
            if is_missing(v):
                return None
            values.append(_require_str(v, "Concat"))
        return "".join(values)

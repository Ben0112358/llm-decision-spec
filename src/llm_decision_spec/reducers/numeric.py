from llm_decision_spec.expressions.base import Expr, _require_expr
from llm_decision_spec.expressions.evaluate import valid_value
from llm_decision_spec.reducers.base import Reducer


def _collect_numeric_values(expr: Expr, rows: list[dict]) -> list:
    values = []
    for event in rows:
        v = valid_value(expr, event)
        if v is not None:
            values.append(v)
    return values


def _ensure_numeric(values: list, expr: Expr) -> None:
    if not all(isinstance(v, (int, float)) for v in values):
        raise TypeError(f"{expr!r} must be numeric")


class Sum(Reducer):
    def __init__(self, expr: Expr):
        self.expr = _require_expr(expr, "expr")

    def evaluate(self, operator, context):
        rows = operator.evaluate(context).data
        values = _collect_numeric_values(self.expr, rows)
        if not values:
            return None
        _ensure_numeric(values, self.expr)
        return sum(values)


class Average(Reducer):
    def __init__(self, expr: Expr):
        self.expr = _require_expr(expr, "expr")

    def evaluate(self, operator, context):
        rows = operator.evaluate(context).data
        values = _collect_numeric_values(self.expr, rows)
        if not values:
            return None
        _ensure_numeric(values, self.expr)
        return sum(values) / len(values)


class Percentile(Reducer):
    def __init__(self, expr: Expr, p: float):
        self.expr = _require_expr(expr, "expr")
        self.p = p
        if p < 0.0 or p > 1.0:
            raise ValueError(f"p must be in [0, 1], got: {p}")

    def evaluate(self, operator, context):
        rows = operator.evaluate(context).data
        values = _collect_numeric_values(self.expr, rows)
        if not values:
            return None
        _ensure_numeric(values, self.expr)
        sorted_values = sorted(values)
        index = int(self.p * (len(sorted_values) - 1))
        return sorted_values[index]


class Max(Reducer):
    def __init__(self, expr: Expr):
        self.expr = _require_expr(expr, "expr")

    def evaluate(self, operator, context):
        rows = operator.evaluate(context).data
        values = _collect_numeric_values(self.expr, rows)
        if not values:
            return None
        _ensure_numeric(values, self.expr)
        return max(values)


class Min(Reducer):
    def __init__(self, expr: Expr):
        self.expr = _require_expr(expr, "expr")

    def evaluate(self, operator, context):
        rows = operator.evaluate(context).data
        values = _collect_numeric_values(self.expr, rows)
        if not values:
            return None
        _ensure_numeric(values, self.expr)
        return min(values)

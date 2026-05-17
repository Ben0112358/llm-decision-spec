from llm_decision_spec.expressions.base import Expr, _require_expr
from llm_decision_spec.expressions.evaluate import valid_value
from llm_decision_spec.reducers.base import Reducer


class Count(Reducer):
    def __init__(self, expr: Expr | None = None):
        if expr is not None:
            self.expr = _require_expr(expr, "expr")
        else:
            self.expr = None

    def evaluate(self, operator, context):
        rows = operator.evaluate(context).data
        if self.expr is None:
            return len(rows)
        return sum(
            1 for event in rows if valid_value(self.expr, event) is not None
        )


class CountDistinct(Reducer):
    def __init__(self, expr: Expr | None = None):
        if expr is not None:
            self.expr = _require_expr(expr, "expr")
        else:
            self.expr = None

    def evaluate(self, operator, context):
        rows = operator.evaluate(context).data
        if self.expr is None:
            return len({context.key(event) for event in rows})
        values = {
            valid_value(self.expr, event)
            for event in rows
            if valid_value(self.expr, event) is not None
        }
        return len(values)

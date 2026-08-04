from llm_decision_spec.expressions.base import Const, Expr
from llm_decision_spec.operators.base import Operator
from llm_decision_spec.util.selection import filter_events_by_predicate


class In(Operator):
    def __init__(self, left: Expr, right: Const):
        values = right.value
        if not isinstance(values, (set, frozenset)):
            raise TypeError("In RHS Const must wrap set or frozenset")
        self.left = left
        self._values = frozenset(values)

    def evaluate(self, context):
        return filter_events_by_predicate(
            context,
            left=self.left,
            match_left=lambda v: v in self._values,
        )


class NotIn(Operator):
    def __init__(self, left: Expr, right: Const):
        values = right.value
        if not isinstance(values, (set, frozenset)):
            raise TypeError("NotIn RHS Const must wrap set or frozenset")
        self.left = left
        self._values = frozenset(values)

    def evaluate(self, context):
        return filter_events_by_predicate(
            context,
            left=self.left,
            match_left=lambda v: v not in self._values,
        )

from llm_decision_spec.expressions.base import Expr
from llm_decision_spec.operators.base import Operator
from llm_decision_spec.operators.predicate import filter_events_by_predicate


class Eq(Operator):
    def __init__(self, left: Expr, right: Expr):
        self.left = left
        self.right = right

    def evaluate(self, context):
        return filter_events_by_predicate(
            context,
            left=self.left,
            right=self.right,
            match=lambda lv, rv: lv == rv,
        )


class Ne(Operator):
    def __init__(self, left: Expr, right: Expr):
        self.left = left
        self.right = right

    def evaluate(self, context):
        return filter_events_by_predicate(
            context,
            left=self.left,
            right=self.right,
            match=lambda lv, rv: lv != rv,
        )


class Gte(Operator):
    def __init__(self, left: Expr, right: Expr):
        self.left = left
        self.right = right

    def evaluate(self, context):
        return filter_events_by_predicate(
            context,
            left=self.left,
            right=self.right,
            match=lambda lv, rv: lv >= rv,
        )


class Lte(Operator):
    def __init__(self, left: Expr, right: Expr):
        self.left = left
        self.right = right

    def evaluate(self, context):
        return filter_events_by_predicate(
            context,
            left=self.left,
            right=self.right,
            match=lambda lv, rv: lv <= rv,
        )


class Gt(Operator):
    def __init__(self, left: Expr, right: Expr):
        self.left = left
        self.right = right

    def evaluate(self, context):
        return filter_events_by_predicate(
            context,
            left=self.left,
            right=self.right,
            match=lambda lv, rv: lv > rv,
        )


class Lt(Operator):
    def __init__(self, left: Expr, right: Expr):
        self.left = left
        self.right = right

    def evaluate(self, context):
        return filter_events_by_predicate(
            context,
            left=self.left,
            right=self.right,
            match=lambda lv, rv: lv < rv,
        )

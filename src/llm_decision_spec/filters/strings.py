import re

from llm_decision_spec.expressions.base import Const, Expr
from llm_decision_spec.operators.base import Operator
from llm_decision_spec.operators.predicate import (
    filter_events_by_predicate,
    filter_events_by_str_binary,
)


class Contains(Operator):
    def __init__(self, left: Expr, right: Expr):
        self.left = left
        self.right = right

    def evaluate(self, context):
        return filter_events_by_str_binary(
            context,
            self.left,
            self.right,
            match=lambda lv, rv: rv in lv,
        )


class StartsWith(Operator):
    def __init__(self, left: Expr, right: Expr):
        self.left = left
        self.right = right

    def evaluate(self, context):
        return filter_events_by_str_binary(
            context,
            self.left,
            self.right,
            match=lambda lv, rv: lv.startswith(rv),
        )


class EndsWith(Operator):
    def __init__(self, left: Expr, right: Expr):
        self.left = left
        self.right = right

    def evaluate(self, context):
        return filter_events_by_str_binary(
            context,
            self.left,
            self.right,
            match=lambda lv, rv: lv.endswith(rv),
        )


class Regex(Operator):
    def __init__(self, left: Expr, pattern: Const):
        if not isinstance(pattern, Const):
            raise TypeError("Regex pattern must be Const")
        if not isinstance(pattern.value, str):
            raise TypeError("Regex pattern Const must wrap str")
        self.left = left
        self._compiled = re.compile(pattern.value)

    def evaluate(self, context):
        return filter_events_by_predicate(
            context,
            left=self.left,
            match_left=lambda v: isinstance(v, str)
            and self._compiled.search(v) is not None,
        )

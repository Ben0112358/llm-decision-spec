from llm_decision_spec.core.context import Context
from llm_decision_spec.core.result import EvaluationResult
from llm_decision_spec.expressions import Expr
from llm_decision_spec.operators.base import Operator
from llm_decision_spec.utils.selection import (
    filter_events_by_context_datetime,
    filter_events_by_event_datetime,
)


class Before(Operator):
    def __init__(self, right: Expr):
        self.right = right

    def evaluate(self, context: Context) -> EvaluationResult:
        return filter_events_by_event_datetime(
            context,
            right=self.right,
            match=lambda event_time, value: event_time <= value,
        )


class StrictlyBefore(Operator):
    def __init__(self, right: Expr):
        self.right = right

    def evaluate(self, context: Context) -> EvaluationResult:
        return filter_events_by_event_datetime(
            context,
            right=self.right,
            match=lambda event_time, value: event_time < value,
        )


class After(Operator):
    def __init__(self, right: Expr):
        self.right = right

    def evaluate(self, context: Context) -> EvaluationResult:
        return filter_events_by_event_datetime(
            context,
            right=self.right,
            match=lambda event_time, value: event_time > value,
        )


class StrictlyAfter(Operator):
    def __init__(self, right: Expr):
        self.right = right

    def evaluate(self, context: Context) -> EvaluationResult:
        return filter_events_by_event_datetime(
            context,
            right=self.right,
            match=lambda event_time, value: event_time >= value,
        )


class EventWithinXDays(Operator):
    def __init__(self, x: int):
        self.x = x

    def evaluate(self, context: Context) -> EvaluationResult:

        return filter_events_by_context_datetime(
            context,
            match=lambda event_time: (
                context.context_datetime - event_time
            ).days
            <= self.x,
        )


class EventBeyondXDays(Operator):
    def __init__(self, x: int):
        self.x = x

    def evaluate(self, context: Context) -> EvaluationResult:

        return filter_events_by_context_datetime(
            context,
            match=lambda event_time: (
                context.context_datetime - event_time
            ).days
            >= self.x,
        )


class EventFromXDaysBackToYDaysBack(Operator):
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

        if self.x < self.y:
            raise ValueError(f"x ({x}) is smaller than y ({y}).")

    def evaluate(self, context: Context) -> EvaluationResult:

        return filter_events_by_context_datetime(
            context,
            match=lambda event_time: (
                context.context_datetime - event_time
            ).days
            <= self.x
            and (context.context_datetime - event_time).days >= self.y,
        )

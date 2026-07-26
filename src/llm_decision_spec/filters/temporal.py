from llm_decision_spec.operators.base import EvaluationResult, Operator
from llm_decision_spec.execution.context import Context
from llm_decision_spec.expressions import Expr
from llm_decision_spec.operators.predicate import filter_events_by_context_datetime, filter_events_by_event_datetime
from dateutil import relativedelta


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


class EventWithinXMonths(Operator):
    def __init__(self, x: int):
        self.x = x

    def evaluate(self, context: Context) -> EvaluationResult:
        cutoff = context.context_datetime - relativedelta(months=self.x)

        return filter_events_by_context_datetime(
            context,
            match=lambda event_time, now: event_time >= cutoff,
        )


class EventStrictlyWithinXMonths(Operator):
    def __init__(self, x: int):
        self.x = x

    def evaluate(self, context: Context) -> EvaluationResult:
        cutoff = context.context_datetime - relativedelta(months=self.x)

        return filter_events_by_context_datetime(
            context,
            match=lambda event_time, now: event_time > cutoff,
        )


class EventBeyondXMonths(Operator):
    def __init__(self, x: int):
        self.x = x

    def evaluate(self, context: Context) -> EvaluationResult:
        cutoff = context.context_datetime - relativedelta(months=self.x)

        return filter_events_by_context_datetime(
            context,
            match=lambda event_time, now: event_time <= cutoff,
        )


class EventStrictlyBeyondXMonths(Operator):
    def __init__(self, x: int):
        self.x = x

    def evaluate(self, context: Context) -> EvaluationResult:
        cutoff = context.context_datetime - relativedelta(months=self.x)

        return filter_events_by_context_datetime(
            context,
            match=lambda event_time, now: event_time < cutoff,
        )
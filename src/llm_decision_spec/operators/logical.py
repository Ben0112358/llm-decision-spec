from llm_decision_spec.core.result import EvaluationResult
from llm_decision_spec.operators.base import Operator
from llm_decision_spec.utils.validate import (
    _require_operator,
    _require_operators,
)


class And(Operator):
    def __init__(self, *children: Operator):
        self.children = _require_operators(children, "And")

    def evaluate(self, context) -> EvaluationResult:
        results = [child.evaluate(context).data for child in self.children]

        if not results:
            return EvaluationResult(data=[])

        id_sets = [set(context.key(event) for event in r) for r in results]
        and_ids = set.intersection(*id_sets)

        index = {}
        for r in results:
            for event in r:
                index[context.key(event)] = event

        data = [index[event_id] for event_id in and_ids]

        return EvaluationResult(data=data)


class Or(Operator):
    def __init__(self, *children: Operator):
        self.children = _require_operators(children, "Or")

    def evaluate(self, context) -> EvaluationResult:
        results = [child.evaluate(context).data for child in self.children]

        if not results:
            return EvaluationResult(data=[])

        or_ids = set().union(
            *(set(context.key(event) for event in r) for r in results)
        )

        index = {}
        for r in results:
            for event in r:
                index[context.key(event)] = event

        data = [index[event_id] for event_id in or_ids]

        return EvaluationResult(data=data)


class Not(Operator):
    def __init__(self, child: Operator):
        self.child = _require_operator(child, "Not child")

    def evaluate(self, context):
        child_data = self.child.evaluate(context).data

        child_ids = {context.key(event) for event in child_data}
        universe = context.events

        data = [
            event for event in universe if context.key(event) not in child_ids
        ]

        return EvaluationResult(data=data)


class Difference(Operator):
    def __init__(self, left: Operator, right: Operator):
        self.left = _require_operator(left, "Difference left")
        self.right = _require_operator(right, "Difference right")

    def evaluate(self, context) -> EvaluationResult:
        left_result = self.left.evaluate(context).data
        right_result = self.right.evaluate(context).data

        right_ids = {context.key(event) for event in right_result}

        data = [
            event
            for event in left_result
            if context.key(event) not in right_ids
        ]

        return EvaluationResult(data=data)

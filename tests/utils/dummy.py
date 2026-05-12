from llm_decision_spec.operators.base import Operator, EvaluationResult

class DummyOperator(Operator):
    def __init__(self, value, evidence=None):
        self._value = value
        self._evidence = evidence or []

    def evaluate(self, context):
        return EvaluationResult(
            value=self._value,
            evidence=self._evidence,
        )
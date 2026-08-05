from llm_decision_spec.core.result import EvaluationResult
from llm_decision_spec.operators.base import Operator


class DummyOperator(Operator):
    def __init__(self, data, metadata=None):
        self._data = data
        self._metadata = metadata or {}

    def evaluate(self, context):
        return EvaluationResult(
            data=self._data,
            metadata=self._metadata,
        )

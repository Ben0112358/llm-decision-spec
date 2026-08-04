from abc import ABC, abstractmethod

from llm_decision_spec.core.result import EvaluationResult


class Operator(ABC):
    @abstractmethod
    def evaluate(self, context) -> EvaluationResult:
        raise NotImplementedError()

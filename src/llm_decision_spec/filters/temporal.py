from llm_decision_spec.operators.base import EvaluationResult, Operator


class Before(Operator):
    def evaluate(self, context) -> EvaluationResult:
        raise NotImplementedError


class After(Operator):
    def evaluate(self, context) -> EvaluationResult:
        raise NotImplementedError


class Between(Operator):
    def evaluate(self, context) -> EvaluationResult:
        raise NotImplementedError

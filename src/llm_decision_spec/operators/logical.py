from llm_decision_spec.operators.base import Operator, EvaluationResult


class And(Operator):
    def __init__(self, *children: Operator):
        self.children = children

    def evaluate(self, context) -> EvaluationResult:
        results = [child.evaluate(context) for child in self.children]

        value = all(r.value for r in results)

        evidence = []
        for r in results:
            evidence.extend(r.evidence)

        return EvaluationResult(
            value=value,
            evidence=evidence
        )
    
class Or(Operator):
    def __init__(self, *children: Operator):
        self.children = children

    def evaluate(self, context) -> EvaluationResult:
        results = [child.evaluate(context) for child in self.children]

        value = any(r.value for r in results)

        evidence = []
        for r in results:
            evidence.extend(r.evidence)

        return EvaluationResult(
            value=value,
            evidence=evidence
        )
    

class Not(Operator):
    def __init__(self, child: Operator):
        self.child = child
    def evaluate(self, context) -> EvaluationResult:
        results = self.child.evaluate(context)

        return EvaluationResult(
            value=not results.value,
            evidence=results.evidence
        )
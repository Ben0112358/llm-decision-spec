from llm_decision_spec.operators.base import Operator, EvaluationResult


class Has(Operator):
    def __init__(self, field):
        self.field = field

    def evaluate(self, context):
        data = []
        for e in context.events:
            if self.field in e:
                data.append(e)

        return EvaluationResult(data=data)


class Missing(Operator):
    def __init__(self, field):
        self.field = field

    def evaluate(self, context):
        data = []
        for e in context.events:
            if self.field not in e:
                data.append(e)

        return EvaluationResult(data=data)

from llm_decision_spec.operators.base import Operator, EvaluationResult



class In(Operator):
    def __init__(self, field, values):
        self.field = field
        self.values = set(values)

    def evaluate(self, context):
        data = []
        for e in context.events:
            v = e.get(self.field)
            if v is None:
                continue
            if v in self.values:
                data.append(e)

        return EvaluationResult(data=data)
    

class NotIn(Operator):
    def __init__(self, field, values):
        self.field = field
        self.values = set(values)

    def evaluate(self, context):
        data = []
        for e in context.events:
            v = e.get(self.field)
            if v is None:
                continue
            if v not in self.values:
                data.append(e)

        return EvaluationResult(data=data)
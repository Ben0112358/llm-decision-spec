from llm_decision_spec.operators.base import Operator, EvaluationResult





class Eq(Operator):
    def __init__(self, field, value):
        self.field = field
        self.value = value

    def evaluate(self, context):
        data = []
        for e in context.events:
            v = e.get(self.field)
            if v is None:
                continue
            if v == self.value:
                data.append(e)

        return EvaluationResult(data=data)
    
class Ne(Operator):
    def __init__(self, field, value):
        self.field = field
        self.value = value

    def evaluate(self, context):
        data = []
        for e in context.events:
            v = e.get(self.field)
            if v is None:
                continue
            if v != self.value:
                data.append(e)

        return EvaluationResult(data=data)

class Gte(Operator):
    def __init__(self, field, value):
        self.field = field
        self.value = value

    def evaluate(self, context):
        data = []
        for e in context.events:
            v = e.get(self.field)
            if v is None:
                continue
            if v >= self.value:
                data.append(e)

        return EvaluationResult(data=data)
    
class Lte(Operator):
    def __init__(self, field, value):
        self.field = field
        self.value = value

    def evaluate(self, context):
        data = []
        for e in context.events:
            v = e.get(self.field)
            if v is None:
                continue
            if v <= self.value:
                data.append(e)

        return EvaluationResult(data=data)
    
class Gt(Operator):
    def __init__(self, field, value):
        self.field = field
        self.value = value

    def evaluate(self, context):
        data = []
        for e in context.events:
            v = e.get(self.field)
            if v is None:
                continue
            if v > self.value:
                data.append(e)

        return EvaluationResult(data=data)
    
    
class Lt(Operator):
    def __init__(self, field, value):
        self.field = field
        self.value = value

    def evaluate(self, context):
        data = []
        for e in context.events:
            v = e.get(self.field)
            if v is None:
                continue
            if v < self.value:
                data.append(e)

        return EvaluationResult(data=data)
    

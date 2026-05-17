from llm_decision_spec.expressions.fields import Field
from llm_decision_spec.operators.base import EvaluationResult, Operator


class Has(Operator):
    def __init__(self, field: Field):
        if not isinstance(field, Field):
            raise TypeError("Has requires Field(...)")
        self.field = field

    def evaluate(self, context):
        name = self.field.name
        data = [e for e in context.events if name in e]
        return EvaluationResult(data=data)


class Missing(Operator):
    def __init__(self, field: Field):
        if not isinstance(field, Field):
            raise TypeError("Missing requires Field(...)")
        self.field = field

    def evaluate(self, context):
        name = self.field.name
        data = [e for e in context.events if name not in e]
        return EvaluationResult(data=data)

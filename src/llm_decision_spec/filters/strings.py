from llm_decision_spec.operators.base import Operator, EvaluationResult
import re


class Contains(Operator):
    def __init__(self, field, substring):
        self.field = field
        self.substring = substring

    def evaluate(self, context):
        data = []
        for e in context.events:
            v = e.get(self.field)
            if not isinstance(v, str):
                continue
            if self.substring in v:
                data.append(e)

        return EvaluationResult(data=data)


class StartsWith(Operator):
    def __init__(self, field, substring):
        self.field = field
        self.substring = substring

    def evaluate(self, context):
        data = []
        for e in context.events:
            v = e.get(self.field)
            if v is None or not isinstance(v, str):
                continue
            if v.startswith(self.substring):
                data.append(e)

        return EvaluationResult(data=data)


class EndsWith(Operator):
    def __init__(self, field, substring):
        self.field = field
        self.substring = substring

    def evaluate(self, context):
        data = []
        for e in context.events:
            v = e.get(self.field)
            if v is None or not isinstance(v, str):
                continue
            if v.endswith(self.substring):
                data.append(e)

        return EvaluationResult(data=data)


class Regex(Operator):
    def __init__(self, field, pattern):
        self.field = field
        self.pattern = re.compile(pattern)

    def evaluate(self, context):
        data = []
        for e in context.events:
            v = e.get(self.field)
            if not isinstance(v, str):
                continue
            if self.pattern.search(v):
                data.append(e)

        return EvaluationResult(data=data)

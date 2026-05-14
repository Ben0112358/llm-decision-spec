from llm_decision_spec.reducers.base import Reducer

class Count(Reducer):
    def __init__(self, field=None):
        self.field = field

    def evaluate(self, operator, context):
        result = operator.evaluate(context).data

        if self.field is None:
            return len(result)

        return sum(1 for tx in result if tx.get(self.field) is not None)

class CountDistinct(Reducer):
    def __init__(self, field=None):
        self.field = field

    def evaluate(self, operator, context):
        result = operator.evaluate(context).data

        if self.field is None:
            return len({context.key(tx) for tx in result})

        values = {
            tx[self.field]
            for tx in result
            if tx.get(self.field) is not None
        }

        return len(values)

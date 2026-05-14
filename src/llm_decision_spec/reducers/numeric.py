from llm_decision_spec.reducers.base import Reducer


class Sum(Reducer):
    def __init__(self, field: str):
        self.field = field

    def evaluate(self, operator, context):
        result = operator.evaluate(context).data

        values = [
            tx.get(self.field)
            for tx in result
            if tx.get(self.field) is not None
        ]

        if not values:
            return None
        
        if not all(isinstance(v, (int, float)) for v in values):
            raise ValueError(f"{self.field} must be numeric")

        return sum(values)

class Average(Reducer):
    def __init__(self, field: str):
        self.field = field

    def evaluate(self, operator, context):
        result = operator.evaluate(context).data

        values = [
            tx.get(self.field)
            for tx in result
            if tx.get(self.field) is not None
        ]

        if not values:
            return None
        
        if not all(isinstance(v, (int, float)) for v in values):
            raise ValueError(f"{self.field} must be numeric")

        return sum(values) / len(values)

class Percentile(Reducer):
    def __init__(self, field: str, p: float):
        self.field = field
        self.p = p

        if p < 0.0 or p > 1.0:
            raise ValueError(f"p must be in [0, 1], got: {p}")

    def evaluate(self, operator, context):
        result = operator.evaluate(context).data

        values = [
            tx.get(self.field)
            for tx in result
            if tx.get(self.field) is not None
        ]

        if not values:
            return None

        if not all(isinstance(v, (int, float)) for v in values):
            raise ValueError(f"{self.field} must be numeric")

        sorted_values = sorted(values)

        index = int(self.p * (len(sorted_values) - 1))
        return sorted_values[index]

class Max(Reducer):
    def __init__(self, field: str):
        self.field = field

    def evaluate(self, operator, context):
        result = operator.evaluate(context).data

        values = [
            tx.get(self.field)
            for tx in result
            if tx.get(self.field) is not None
        ]

        if not values:
            return None
        
        if not all(isinstance(v, (int, float)) for v in values):
            raise ValueError(f"{self.field} must be numeric")

        return max(values)

class Min(Reducer):
    def __init__(self, field: str):
        self.field = field

    def evaluate(self, operator, context):
        result = operator.evaluate(context).data

        values = [
            tx.get(self.field)
            for tx in result
            if tx.get(self.field) is not None
        ]

        if not values:
            return None
        
        if not all(isinstance(v, (int, float)) for v in values):
            raise ValueError(f"{self.field} must be numeric")

        return min(values)
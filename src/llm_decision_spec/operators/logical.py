from llm_decision_spec.operators.base import Operator, EvaluationResult


class And(Operator):
    def __init__(self, *children: Operator):
        self.children = children

    def evaluate(self, context) -> EvaluationResult:
        results = [child.evaluate(context).data for child in self.children]

        if not results:
            return EvaluationResult(data=[])

        id_sets = [set(context.key(tx) for tx in r) for r in results]
        and_ids = set.intersection(*id_sets)

        index = {}
        for r in results:
            for tx in r:
                index[context.key(tx)] = tx

        data = [index[tx_id] for tx_id in and_ids]

        return EvaluationResult(data=data)


class Or(Operator):
    def __init__(self, *children: Operator):
        self.children = children

    def evaluate(self, context) -> EvaluationResult:
        results = [child.evaluate(context).data for child in self.children]

        if not results:
            return EvaluationResult(data=[])

        or_ids = set().union(*(set(context.key(tx) for tx in r) for r in results))

        index = {}
        for r in results:
            for tx in r:
                index[context.key(tx)] = tx

        data = [index[tx_id] for tx_id in or_ids]

        return EvaluationResult(data=data)


class Not(Operator):
    def __init__(self, child: Operator):
        self.child = child

    def evaluate(self, context):
        child_data = self.child.evaluate(context).data

        child_ids = {context.key(tx) for tx in child_data}
        universe = context.transactions

        data = [tx for tx in universe if context.key(tx) not in child_ids]

        return EvaluationResult(data=data)


class Difference(Operator):
    def __init__(self, left: Operator, right: Operator):
        self.left = left
        self.right = right

    def evaluate(self, context) -> EvaluationResult:
        left_result = self.left.evaluate(context).data
        right_result = self.right.evaluate(context).data

        right_ids = {context.key(tx) for tx in right_result}

        data = [
            tx for tx in left_result
            if context.key(tx) not in right_ids
        ]

        return EvaluationResult(data=data)
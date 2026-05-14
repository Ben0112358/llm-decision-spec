from llm_decision_spec.reducers.base import Reducer
from llm_decision_spec.reducers.counting import Count

class Exists(Reducer):
    def evaluate(self, operator, context):
        return Count().evaluate(operator, context) > 0
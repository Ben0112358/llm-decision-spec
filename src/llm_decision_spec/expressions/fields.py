from llm_decision_spec.expressions.base import Expr


class Field(Expr):
    def __init__(self, name: str):
        self._name = name

    @property
    def name(self) -> str:
        return self._name

    def eval(self, event: dict):
        return event.get(self._name)

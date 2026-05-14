from abc import ABC, abstractmethod


class Reducer(ABC):
    def evaluate(self, operator, context):
        raise NotImplementedError
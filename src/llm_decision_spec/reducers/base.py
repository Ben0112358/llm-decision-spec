from abc import ABC, abstractmethod


class Reducer(ABC):
    @abstractmethod
    def evaluate(self, operator, context):
        raise NotImplementedError

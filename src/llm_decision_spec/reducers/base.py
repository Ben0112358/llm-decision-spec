from abc import ABC, abstractmethod


class Reducer(ABC):
    def __init__(self, source):
        self.source = source

    @abstractmethod
    def evaluate(self, context):
        raise NotImplementedError()
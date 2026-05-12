from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any


@dataclass
class EvaluationResult:
    value: Any
    evidence: list[dict] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)


class Operator(ABC):
    
    @abstractmethod
    def evaluate(self, context) -> EvaluationResult:
        raise NotImplementedError

    def __call__(self, context) -> EvaluationResult:
        return self.evaluate(context)

    def __add__(self, other: "Operator") -> "Operator":
        from .logical import Or
        return Or(self, other)

    def __mul__(self, other: "Operator") -> "Operator":
        from .logical import And
        return And(self, other)

    def __sub__(self, other: "Operator") -> "Operator":
        from .logical import And, Not
        return And(self, Not(other))
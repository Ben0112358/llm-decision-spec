from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any


@dataclass
class EvaluationResult:
    data: list[dict]
    metadata: dict[str, Any] = field(default_factory=dict)


class Operator(ABC):
    @abstractmethod
    def evaluate(self, context) -> EvaluationResult:
        raise NotImplementedError()
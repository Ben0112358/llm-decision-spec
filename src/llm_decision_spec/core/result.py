from dataclasses import dataclass, field
from typing import Any


@dataclass
class EvaluationResult:
    data: list[dict]
    metadata: dict[str, Any] = field(default_factory=dict)

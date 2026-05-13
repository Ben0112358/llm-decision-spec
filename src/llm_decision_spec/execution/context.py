from dataclasses import dataclass
from collections.abc import Callable


@dataclass
class Context:
    transactions: list[dict]
    key_fn: Callable[[dict], object]

    def key(self, tx: dict) -> object:
        return self.key_fn(tx)

    def keys(self, rows: list[dict]) -> set:
        return {self.key(tx) for tx in rows}

    def index(self, rows: list[list[dict]]) -> dict:
        out = {}
        for group in rows:
            for tx in group:
                out[self.key(tx)] = tx
        return out

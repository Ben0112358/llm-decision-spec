from dataclasses import dataclass
from collections.abc import Callable
from datetime import datetime


@dataclass
class Context:
    events: list[dict]
    key_fn: Callable[[dict], object]
    datetime_fn: Callable[[dict], datetime]

    def datetime(self, event: dict) -> datetime:
        return self.datetime_fn(event)

    def key(self, event: dict) -> object:
        return self.key_fn(event)

    def keys(self, rows: list[dict]) -> set:
        return {self.key(event) for event in rows}

    def index(self, rows: list[list[dict]]) -> dict:
        out = {}
        for group in rows:
            for event in group:
                out[self.key(event)] = event
        return out

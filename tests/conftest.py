import pytest
from llm_decision_spec.execution.context import Context


@pytest.fixture
def universe():
    return [
        {"id": 3, "amount": 50, "currency": "SEK", "merchant": "A"},
        {"id": 1, "amount": 200, "currency": "USD", "merchant": "B"},
        {"id": 2, "amount": 100, "currency": "SEK", "merchant": "A"},
    ]


@pytest.fixture
def context(universe):
    return Context(events=universe, key_fn=lambda event: event["id"])

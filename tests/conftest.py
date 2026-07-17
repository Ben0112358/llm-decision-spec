import pytest
from llm_decision_spec.execution.context import Context
from datetime import datetime


@pytest.fixture
def universe():
    return [
        {
            "id": 3,
            "amount": 50,
            "currency": "SEK",
            "merchant": "A",
            "datetime": datetime(2026, 1, 1),
        },
        {
            "id": 1,
            "amount": 200,
            "currency": "USD",
            "merchant": "B",
            "datetime": datetime(2026, 1, 2, 12, 0, 0),
        },
        {
            "id": 2,
            "amount": 100,
            "currency": "SEK",
            "merchant": "A",
            "datetime": datetime(2026, 1, 3, 12, 0, 0),
        },
    ]


@pytest.fixture
def context(universe):
    return Context(
        events=universe,
        key_fn=lambda event: event["id"],
        datetime_fn=lambda event: event["datetime"],
    )

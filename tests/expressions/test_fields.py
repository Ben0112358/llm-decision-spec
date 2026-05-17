from llm_decision_spec.expressions import Field
from llm_decision_spec.filters.presence import Has


def test_field_returns_value():
    event = {"amount": 100}
    assert Field("amount").eval(event) == 100


def test_field_missing_key_returns_none():
    event = {"amount": 100}
    assert Field("nonexistent").eval(event) is None


def test_field_key_present_value_none():
    event = {"amount": None}
    assert Field("amount").eval(event) is None
    assert "amount" in event


def test_has_key_present_value_none():
    event = {"id": 1, "amount": None}
    from llm_decision_spec.execution.context import Context

    ctx = Context(events=[event], key_fn=lambda e: e["id"])
    result = Has(Field("amount")).evaluate(ctx)
    assert len(result.data) == 1

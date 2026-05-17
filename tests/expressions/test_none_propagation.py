import pytest

from llm_decision_spec.execution.context import Context
from llm_decision_spec.expressions import Const, Field
from llm_decision_spec.filters.comparison import Eq, Gt
from llm_decision_spec.filters.membership import In
from llm_decision_spec.filters.strings import Contains, Regex


def _ctx(events):
    return Context(events=events, key_fn=lambda e: e["id"])


def test_predicate_skip_on_none_never_raises():
    ctx = _ctx([{"id": 1, "a": None}, {"id": 2}])
    for op in [
        Gt(Field("a"), Const(1)),
        Eq(Field("missing"), Const("x")),
        In(Field("a"), Const(frozenset({1}))),
        Contains(Field("a"), Const("x")),
        Regex(Field("a"), Const(".*")),
    ]:
        result = op.evaluate(ctx)
        assert isinstance(result.data, list)


@pytest.mark.parametrize(
    "op_factory",
    [
        lambda: Gt(Field("a"), Const(1)),
        lambda: In(Field("a"), Const(frozenset({1, 2}))),
    ],
)
def test_predicate_missing_field_skips(op_factory):
    ctx = _ctx([{"id": 1}])
    result = op_factory().evaluate(ctx)
    assert result.data == []

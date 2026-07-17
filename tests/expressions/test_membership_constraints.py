import pytest

from llm_decision_spec.expressions import Const, Field
from llm_decision_spec.filters.membership import In


def test_in_rejects_const_non_collection():
    with pytest.raises(TypeError, match="set or frozenset"):
        In(Field("x"), Const("not a set"))

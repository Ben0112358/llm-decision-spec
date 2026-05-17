import pytest

from llm_decision_spec.expressions import Const, Field
from llm_decision_spec.filters.membership import In


def test_in_rejects_non_const_rhs():
    with pytest.raises(TypeError, match="Const"):
        In(Field("x"), Field("y"))


def test_in_rejects_const_non_collection():
    with pytest.raises(TypeError, match="set or frozenset"):
        In(Field("x"), Const("not a set"))

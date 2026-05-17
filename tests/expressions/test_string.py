from llm_decision_spec.expressions import (
    Concat,
    Const,
    Field,
    Length,
    Lower,
    Upper,
)


def test_lower_upper():
    event = {"name": "Hello"}
    assert Lower(Field("name")).eval(event) == "hello"
    assert Upper(Field("name")).eval(event) == "HELLO"


def test_length():
    event = {"name": "abc"}
    assert Length(Field("name")).eval(event) == 3


def test_concat():
    event = {"a": "foo", "b": "bar"}
    assert Concat(Field("a"), Const("-"), Field("b")).eval(event) == "foo-bar"


def test_concat_propagates_none():
    event = {"a": "foo"}
    assert Concat(Field("a"), Field("b")).eval(event) is None

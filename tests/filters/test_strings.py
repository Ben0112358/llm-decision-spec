import pytest

from llm_decision_spec.filters.strings import Contains, Regex
from llm_decision_spec.operators.logical import And
from llm_decision_spec.filters.comparison import Gt


def ids(result):
    return sorted(e["id"] for e in result.data)


def test_contains_matches_substring(context):
    op = Contains("merchant", "A")

    result = op.evaluate(context)

    assert ids(result) == [2, 3]


def test_contains_no_match(context):
    op = Contains("merchant", "XYZ")

    result = op.evaluate(context)

    assert ids(result) == []


def test_contains_missing_field_excluded(context):
    op = Contains("does_not_exist", "foo")

    result = op.evaluate(context)

    assert ids(result) == []


def test_contains_non_string_excluded(context):
    op = Contains("amount", "50")

    result = op.evaluate(context)

    assert ids(result) == []



def test_regex_matches_pattern(context):
    op = Regex("currency", r"S.K")

    result = op.evaluate(context)

    assert ids(result) == [2, 3]


def test_regex_no_match(context):
    op = Regex("merchant", r"^Z")

    result = op.evaluate(context)

    assert ids(result) == []


def test_regex_missing_field_excluded(context):
    op = Regex("does_not_exist", r".*")

    result = op.evaluate(context)

    assert ids(result) == []


def test_regex_non_string_excluded(context):
    op = Regex("amount", r"\d+")

    result = op.evaluate(context)

    assert ids(result) == []



def test_contains_with_and(context):
    op = And(
        Contains("merchant", "A"),
        Gt("amount", 60),
    )

    result = op.evaluate(context)

    assert ids(result) == [2]
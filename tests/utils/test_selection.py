import pytest
from datetime import datetime

from llm_decision_spec.core.context import Context
from llm_decision_spec.expressions import Const, Field
from llm_decision_spec.utils.selection import (
    filter_events_by_predicate,
    filter_events_by_str_binary,
    filter_events_by_context_datetime,
    filter_events_by_event_datetime,
)
from tests.conftest import CONTEXT_DATETIME
from tests.helpers.assertions import assert_event_ids


def test_binary_predicate_filters_matching_events(context):
    result = filter_events_by_predicate(
        context,
        left=Field("currency"),
        right=Const("SEK"),
        match=lambda lv, rv: lv == rv,
    )
    assert_event_ids(result, [2, 3], context)


def test_binary_predicate_skips_when_either_side_missing(context):
    result = filter_events_by_predicate(
        context,
        left=Field("missing"),
        right=Const(1),
        match=lambda lv, rv: lv == rv,
    )
    assert_event_ids(result, [], context)


def test_binary_predicate_raises_without_match_or_right(context):
    with pytest.raises(ValueError, match="binary predicate requires right and match"):
        filter_events_by_predicate(context, left=Field("amount"))


def test_unary_match_left_filters_without_right(context):
    result = filter_events_by_predicate(
        context,
        left=Field("currency"),
        match_left=lambda v: v in {"SEK", "USD"},
    )
    assert_event_ids(result, [1, 2, 3], context)


def test_unary_match_left_skips_missing_left(context):
    result = filter_events_by_predicate(
        context,
        left=Field("missing"),
        match_left=lambda v: True,
    )
    assert_event_ids(result, [], context)


def test_match_left_takes_precedence_over_binary_args(context):
    # match_left wins; right/match are ignored
    result = filter_events_by_predicate(
        context,
        left=Field("amount"),
        right=Const(999),
        match=lambda lv, rv: False,
        match_left=lambda v: v > 100,
    )
    assert_event_ids(result, [1], context)  # only id=1 has amount 200

def test_str_binary_matches_strings(context):
    result = filter_events_by_str_binary(
        context,
        Field("merchant"),
        Const("A"),
        match=lambda lv, rv: rv in lv,
    )
    assert_event_ids(result, [2, 3], context)


def test_str_binary_skips_non_string_operands(context):
    result = filter_events_by_str_binary(
        context,
        Field("amount"),   # int
        Const("50"),       # str
        match=lambda lv, rv: str(lv) == rv,
    )
    assert_event_ids(result, [], context)


def test_str_binary_skips_missing_values(context):
    result = filter_events_by_str_binary(
        context,
        Field("missing"),
        Const("x"),
        match=lambda lv, rv: True,
    )
    assert_event_ids(result, [], context)


def test_context_datetime_filters_by_event_time(context):
    result = filter_events_by_context_datetime(
        context,
        match=lambda dt: dt < CONTEXT_DATETIME,
    )
    assert_event_ids(result, [1, 2, 3], context)

def test_context_datetime_uses_context_fn_not_raw_field():
    event = {"id": 42, "datetime": datetime(2099, 1, 1)}
    ctx = Context(
        events=[event],
        event_key_fn=lambda e: e["id"],
        event_datetime_fn=lambda e: datetime(2020, 1, 1),
        context_datetime=datetime(2026, 1, 1),
    )
    result = filter_events_by_context_datetime(
        ctx,
        match=lambda dt: dt.year == 2020,
    )
    assert_event_ids(result, [42], ctx)

def test_event_datetime_passes_event_time_and_right_value(context):
    t_early = datetime(2025, 12, 31)
    result = filter_events_by_event_datetime(
        context,
        right=Const(t_early),
        match=lambda event_time, rv: event_time > rv,
    )
    assert_event_ids(result, [1, 2, 3], context)

    t_mid = datetime(2026, 1, 2, 12, 0, 0)
    result = filter_events_by_event_datetime(
        context,
        right=Const(t_mid),
        match=lambda event_time, rv: event_time > rv,
    )
    assert_event_ids(result, [2], context)


def test_event_datetime_skips_missing_right(context):
    result = filter_events_by_event_datetime(
        context,
        right=Field("missing"),
        match=lambda event_time, rv: True,
    )
    assert_event_ids(result, [], context)
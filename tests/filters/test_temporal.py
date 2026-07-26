import pytest
from datetime import datetime

from llm_decision_spec.expressions.base import Const
from llm_decision_spec.filters.temporal import (
    After,
    Before,
    StrictlyAfter,
    StrictlyBefore,
    EventWithinXDays,
    EventBeyondXDays,
    EventFromXDaysBackToYDaysBack,
)
from llm_decision_spec.operators.logical import And
import math

# Fixture event times (see conftest universe):
#   id 3 → 2026-01-01 (3 days back)
#   id 1 → 2026-01-02 12:00 (1 days back)
#   id 2 → 2026-01-03 12:00 (0 days back)
#   context datetime is 2026-01-04 11:00
T_MID = datetime(2026, 1, 2, 12, 0, 0)
T_LATE = datetime(2026, 1, 3, 12, 0, 0)
T_BETWEEN = datetime(2026, 1, 3, 0, 0, 0)


def ids(result):
    return sorted(e["id"] for e in result.data)


def test_strictly_before_open_right(context):
    """(-inf, a)  →  event_time < a"""
    op = StrictlyBefore(Const(T_BETWEEN))
    assert ids(op.evaluate(context)) == [1, 3]


def test_before_closed_right(context):
    """(-inf, a]  →  event_time <= a"""
    op = Before(Const(T_BETWEEN))
    assert ids(op.evaluate(context)) == [1, 3]


def test_after_open_left(context):
    """(a, inf)  →  event_time > a"""
    op = After(Const(T_MID))
    assert ids(op.evaluate(context)) == [2]


def test_strictly_after_closed_left(context):
    """[a, inf)  →  event_time >= a"""
    op = StrictlyAfter(Const(T_MID))
    assert ids(op.evaluate(context)) == [1, 2]


def test_open_interval(context):
    """(a, b)  →  a < event_time < b"""
    op = And(
        After(Const(T_MID)),
        StrictlyBefore(Const(T_LATE)),
    )
    assert ids(op.evaluate(context)) == []


def test_open_closed_interval(context):
    """(a, b]  →  a < event_time <= b"""
    op = And(
        After(Const(T_MID)),
        Before(Const(T_LATE)),
    )
    assert ids(op.evaluate(context)) == [2]


def test_closed_open_interval(context):
    """[a, b)  →  a <= event_time < b"""
    op = And(
        StrictlyAfter(Const(T_MID)),
        StrictlyBefore(Const(T_LATE)),
    )
    assert ids(op.evaluate(context)) == [1]


def test_closed_interval(context):
    """[a, b]  →  a <= event_time <= b"""
    op = And(
        StrictlyAfter(Const(T_MID)),
        Before(Const(T_LATE)),
    )
    assert ids(op.evaluate(context)) == [1, 2]


def test_boundary_included_only_on_closed_side(context):
    """At exactly a"""
    assert ids(Before(Const(T_MID)).evaluate(context)) == [1, 3]
    assert ids(StrictlyBefore(Const(T_MID)).evaluate(context)) == [3]
    assert ids(StrictlyAfter(Const(T_MID)).evaluate(context)) == [1, 2]
    assert ids(After(Const(T_MID)).evaluate(context)) == [2]


@pytest.mark.parametrize(
    "x, y, within_expected, beyond_expected",
    [
        (-1, -1, [], [1, 2, 3]),
        (0, 0, [2], [1, 2, 3]),
        (1, 0, [1, 2], [1, 2, 3]),
        (3, 2, [1, 2, 3], [3]),
        (math.inf, 2, [1, 2, 3], [3]),
        (4, 3, [1, 2, 3], [3]),
    ],
)
def test_within_beyond_between(
    context, x, y, within_expected, beyond_expected
):
    within = ids(EventWithinXDays(x=x).evaluate(context))
    beyond = ids(EventBeyondXDays(x=y).evaluate(context))
    between = ids(EventFromXDaysBackToYDaysBack(x=x, y=y).evaluate(context))

    assert within == within_expected
    assert beyond == beyond_expected
    assert between == sorted(set(within_expected) & set(beyond_expected))


def test_between_raises_when_x_smaller_than_y(context):
    with pytest.raises(ValueError, match="smaller than"):
        EventFromXDaysBackToYDaysBack(x=2, y=3).evaluate(context)

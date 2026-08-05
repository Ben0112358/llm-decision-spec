def assert_event_ids(result, expected, context):
    assert {context.key(event) for event in result.data} == set(expected)

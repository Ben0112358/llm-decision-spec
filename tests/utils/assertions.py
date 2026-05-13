def assert_tx_ids(result, expected, ctx):
    assert {ctx.key(tx) for tx in result.data} == set(expected)
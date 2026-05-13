from typing import Any

def tx_ids(ids: list[int]) -> list[dict[str, Any]]:
    return [{"id": i} for i in ids]
import json

from typing import Any
from .normalizer import normalize


def canonical_json(
    data: Any,
    *,
    decimal_places: int | None = None,
) -> str:
    kwargs = {}
    if decimal_places is not None:
        kwargs["decimal_places"] = decimal_places
    normalized = normalize(data, **kwargs)

    return json.dumps(
        normalized,
        ensure_ascii=False,
        separators=(',', ':'),
        sort_keys=True,
    )

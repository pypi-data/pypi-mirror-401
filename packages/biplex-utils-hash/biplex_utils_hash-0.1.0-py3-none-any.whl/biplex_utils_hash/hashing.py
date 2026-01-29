import hashlib

from typing import Any
from .json import canonical_json


def sha256_from_data(
    data: Any,
    *,
    decimal_places: int | None = None,
) -> str:
    return hashlib.sha256(
        canonical_json(
            data,
            decimal_places=decimal_places,
        ).encode("utf-8")
    ).hexdigest()

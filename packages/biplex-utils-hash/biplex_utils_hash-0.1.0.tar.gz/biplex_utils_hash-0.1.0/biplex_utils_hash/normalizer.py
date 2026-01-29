import uuid as uuid_module
from datetime import datetime, date
from decimal import Decimal, ROUND_HALF_UP
from typing import Any

DEFAULT_DECIMAL_PLACES = 6


def normalize(
    obj: Any,
    *,
    decimal_places: int = DEFAULT_DECIMAL_PLACES,
) -> Any:
    if isinstance(obj, dict):
        return {
            str(k): normalize(v, decimal_places=decimal_places)
            for k, v in sorted(obj.items(), key=lambda x: str(x[0]))
        }

    if isinstance(obj, (list, tuple)):
        return [
            normalize(v, decimal_places=decimal_places)
            for v in obj
        ]

    if isinstance(obj, (set, frozenset)):
        return [
            normalize(v, decimal_places=decimal_places)
            for v in sorted(obj, key=lambda x: str(x))
        ]

    if isinstance(obj, float):
        return normalize(
            Decimal(str(obj)),
            decimal_places=decimal_places,
        )

    if isinstance(obj, Decimal):
        q = Decimal(10) ** -decimal_places
        return format(
            obj.quantize(q, rounding=ROUND_HALF_UP),
            f".{decimal_places}f",
        )

    if isinstance(obj, datetime):
        return obj.isoformat()

    if isinstance(obj, date):
        return obj.isoformat()

    if isinstance(obj, uuid_module.UUID):
        return str(obj)

    return obj

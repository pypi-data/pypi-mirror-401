import uuid

from typing import Any
from .json import canonical_json


def uuid5_from_data(
    data: Any,
    *,
    namespace: uuid.UUID = uuid.NAMESPACE_OID,
    decimal_places: int | None = None,
) -> uuid.UUID:
    return uuid.uuid5(
        namespace,
        canonical_json(
            data,
            decimal_places=decimal_places,
        ),
    )

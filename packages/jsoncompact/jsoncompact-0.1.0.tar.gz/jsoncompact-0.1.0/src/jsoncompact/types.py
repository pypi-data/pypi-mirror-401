from collections.abc import Mapping, Sequence
from typing import TypeAlias

# See reference: https://docs.python.org/3/library/json.html#json-to-py-table

PyJsonType: TypeAlias = (
    Mapping[str, "PyJsonType"] | Sequence["PyJsonType"] | str | int | float | bool | None
)

JsonSchema: TypeAlias = Mapping[str, PyJsonType] | None | bool

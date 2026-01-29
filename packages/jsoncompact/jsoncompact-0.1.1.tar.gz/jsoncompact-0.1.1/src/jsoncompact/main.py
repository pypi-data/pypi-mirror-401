import contextlib
import json

from jsoncompact.serde import Deserializer, Serializer
from jsoncompact.types import JsonSchema, PyJsonType

orjson = None
ormsgpack = None

with contextlib.suppress(ImportError):
    import orjson

with contextlib.suppress(ImportError):
    import ormsgpack


def serialize(value: PyJsonType, schema: JsonSchema) -> tuple[bytes, list]:
    serializer = Serializer()
    return serializer.serialize(value, schema)


def deserialize(field_list: bytes, data_list: list, schema: JsonSchema) -> PyJsonType:
    serializer = Deserializer()
    return serializer.deserialize(field_list, data_list, schema)


def serialize_json(value: PyJsonType, schema: JsonSchema) -> str:
    field_list, data_list = serialize(value, schema)
    return json.dumps([field_list, data_list])


def deserialize_json(json_data: str, schema: JsonSchema) -> PyJsonType:
    field_list, data_list = json.loads(json_data)
    return deserialize(field_list, data_list, schema)


def serialize_orjson(value: PyJsonType, schema: JsonSchema) -> bytes:
    if orjson is None:
        err = "Package orjson not found"
        raise ModuleNotFoundError(err)
    field_list, data_list = serialize(value, schema)
    return orjson.dumps([field_list, data_list])


def deserialize_orjson(json_data: bytes, schema: JsonSchema) -> PyJsonType:
    if orjson is None:
        err = "Package orjson not found"
        raise ModuleNotFoundError(err)
    field_list, data_list = orjson.loads(json_data)
    return deserialize(field_list, data_list, schema)


def serialize_ormsgpack(value: PyJsonType, schema: JsonSchema) -> bytes:
    if ormsgpack is None:
        err = "Package ormsgpack not found"
        raise ModuleNotFoundError(err)
    field_list, data_list = serialize(value, schema)
    return ormsgpack.packb([field_list, data_list])


def deserialize_ormsgpack(json_data: bytes, schema: JsonSchema) -> PyJsonType:
    if ormsgpack is None:
        err = "Package ormsgpack not found"
        raise ModuleNotFoundError(err)
    field_list, data_list = ormsgpack.unpackb(json_data)
    return deserialize(field_list, data_list, schema)

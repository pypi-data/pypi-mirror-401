from collections import deque

from jsoncompact.types import JsonSchema, PyJsonType

# Note on use of type:ignore - aspects of JSON schemas do not have explicit type checks due to
# being presumed are valid. Validation of JSON schemas is outside the scope of this library.
# Type checks are only for data that is being encoded/decoded.

BYTELEN = 8


class BinaryCounter:
    value: list[int]
    buf_index: int
    buffer: str

    def __init__(self) -> None:
        self.value = []
        self.buf_index = 0
        self.buffer = ""

    def add_pos(self) -> None:
        self.buffer += "1"
        self.buf_index += 1
        if self.buf_index == BYTELEN:
            self.value.append(int(self.buffer, 2))
            self.buffer = ""
            self.buf_index = 0

    def add_neg(self) -> None:
        self.buffer += "0"
        self.buf_index += 1
        if self.buf_index == BYTELEN:
            self.value.append(int(self.buffer, 2))
            self.buffer = ""
            self.buf_index = 0

    def to_bytes(self) -> bytes:
        if self.buffer:
            self.value.append(int(self.buffer.ljust(8, "0"), 2))
        return bytes(self.value)


class BinaryIterator:
    value: list[int]
    buffer: str
    buffer_index: int

    def __init__(self, bytes_in: bytes) -> None:
        self.value = list(reversed(bytes_in))
        self.buffer_index = BYTELEN

    def pop_bool(self) -> bool:
        if self.buffer_index == BYTELEN:
            self.fill_buffer()
        output = bool(int(self.buffer[self.buffer_index]))
        self.buffer_index += 1
        return output

    def fill_buffer(self) -> None:
        self.buffer_index = 0
        self.buffer = format(self.value.pop(), "b").rjust(8, "0")


class Serializer:
    SUB_COMPACT_ITERABLES: bool
    SUB_COMPACT_MAPPINGS: bool

    def __init__(self) -> None:
        self.SUB_COMPACT_ITERABLES = True
        self.SUB_COMPACT_MAPPINGS = True

    def serialize(
        self, value: PyJsonType, schema: JsonSchema
    ) -> tuple[bytes, list]:
        field_list = BinaryCounter()
        data_list = []
        if not isinstance(schema, dict):
            schema = None
            defs = {}
        else:
            defs: dict[str, dict[str, PyJsonType]] = schema.get("$defs", {})  # type: ignore
        self.serialize_var(value, schema, defs, field_list, data_list)
        return field_list.to_bytes(), data_list

    def serialize_model(
        self,
        var: dict[str, PyJsonType],
        var_schema: dict[str, PyJsonType],
        schema_defs: dict[str, dict[str, PyJsonType]],
        field_list: BinaryCounter,
        data_list: list[PyJsonType],
    ) -> None:
        properties: dict[str, dict[str, PyJsonType]] = var_schema["properties"]  # type: ignore
        valid = any(x in var for x in properties)
        if not valid:
            field_list.add_neg()
            return None
        field_list.add_pos()
        for fieldname, field_schema in properties.items():
            if fieldname in var:
                field_list.add_pos()
                self.serialize_var(var[fieldname], field_schema, schema_defs, field_list, data_list)
            else:
                field_list.add_neg()

    def serialize_array(
        self,
        var: list[PyJsonType],
        var_schema: dict[str, PyJsonType],
        schema_defs: dict[str, dict[str, PyJsonType]],
        field_list: BinaryCounter,
        data_list: list[PyJsonType],
    ) -> None:
        if var:
            sub_type = var_schema.get("items")
            if not isinstance(sub_type, dict):
                sub_type = None
            field_list.add_pos()
            data_list.append(0)
            data_len = len(data_list)
            i = 0
            for v in var:
                i += 1
                if self.SUB_COMPACT_ITERABLES and sub_type is not None:
                    self.serialize_var(v, sub_type, schema_defs, field_list, data_list)
                else:
                    data_list.append(v)
            data_list[data_len - 1] = i
            return None
        field_list.add_neg()

    def serialize_object(
        self,
        var: dict[str, PyJsonType],
        var_schema: dict[str, PyJsonType],
        schema_defs: dict[str, dict[str, PyJsonType]],
        field_list: BinaryCounter,
        data_list: list[PyJsonType],
    ) -> None:
        if var:
            sub_type = var_schema.get("additionalProperties")
            if not isinstance(sub_type, dict):
                sub_type = None
            field_list.add_pos()
            data_list.append(0)
            data_len = len(data_list)
            i = 0
            for k, v in var.items():
                i += 1
                data_list.append(k)
                if self.SUB_COMPACT_MAPPINGS and sub_type is not None:
                    self.serialize_var(v, sub_type, schema_defs, field_list, data_list)
                else:
                    data_list.append(v)
            data_list[data_len - 1] = i
        field_list.add_neg()

    def serialize_var(
        self,
        var: PyJsonType,
        var_schema: dict[str, PyJsonType] | None,
        schema_defs: dict[str, dict[str, PyJsonType]],
        field_list: BinaryCounter,
        data_list: list[PyJsonType],
    ) -> None:
        if var_schema is None:
            data_list.append(var)
            return None
        if "$ref" in var_schema:
            ref = var_schema["$ref"].removeprefix("#/$defs/")  # type: ignore
            if ref not in schema_defs:
                err = f"Could not find definition for ref {ref}"
                raise ValueError(err)
            var_schema = schema_defs[ref]
        var_type = var_schema.get("type")
        if var_type == "object":
            if not isinstance(var, dict):
                err = f"Expected python type for object is dict, instead recieved {type(var)}"
                raise TypeError(err)
            if "properties" in var_schema:
                self.serialize_model(var, var_schema, schema_defs, field_list, data_list)
            else:
                self.serialize_object(var, var_schema, schema_defs, field_list, data_list)
        elif var_type == "array":
            if not isinstance(var, list):
                err = f"Expected python type for array is list, instead recieved {type(var)}"
                raise TypeError(err)
            self.serialize_array(var, var_schema, schema_defs, field_list, data_list)
        else:
            data_list.append(var)


class Deserializer:
    SUB_COMPACT_ITERABLES: bool
    SUB_COMPACT_MAPPINGS: bool

    def __init__(self) -> None:
        self.SUB_COMPACT_ITERABLES = True
        self.SUB_COMPACT_MAPPINGS = True

    def deserialize(self, field_list: bytes, data_list: list, schema: JsonSchema) -> PyJsonType:
        if not isinstance(schema, dict):
            schema = None
            defs = {}
        else:
            defs:dict[str, dict] = schema.get("$defs", {}) # type: ignore
        binary_iterator = BinaryIterator(field_list)
        return self.deserialize_var(schema, defs, binary_iterator, deque(data_list))

    def deserialize_model(
        self,
        var_schema: dict[str, PyJsonType],
        schema_defs: dict[str, dict],
        field_list: BinaryIterator,
        data_list: deque[PyJsonType],
    ) -> dict:
        field_bool = field_list.pop_bool()
        if not field_bool:
            return {}
        model_data = {}
        for fieldname, field_schema in var_schema["properties"].items():  # type: ignore
            field_bool = field_list.pop_bool()
            if field_bool:
                model_data[fieldname] = self.deserialize_var(
                    field_schema, # type: ignore
                    schema_defs,
                    field_list,
                    data_list,
                )
        return model_data

    def deserialize_var(
        self,
        var_schema: dict[str, PyJsonType] | None,
        schema_defs: dict[str, dict],
        field_list: BinaryIterator,
        data_list: deque[PyJsonType],
    ) -> PyJsonType:
        if var_schema is None:
            return data_list.popleft()
        if "$ref" in var_schema:
            ref = var_schema["$ref"].removeprefix("#/$defs/")  # type: ignore
            if ref not in schema_defs:
                err = f"Could not find definition for ref {ref}"
                raise ValueError(err)
            var_schema = schema_defs[ref]
        var_type = var_schema.get("type")
        if var_type == "object":
            if "properties" in var_schema:
                return self.deserialize_model(var_schema, schema_defs, field_list, data_list)
            return self.deserialize_object(var_schema, schema_defs, field_list, data_list)
        if var_type == "array":
            return self.deserialize_array(var_schema, schema_defs, field_list, data_list)
        return data_list.popleft()

    def deserialize_array(
        self,
        var_schema: dict[str, PyJsonType],
        schema_defs: dict[str, dict],
        field_list: BinaryIterator,
        data_list: deque[PyJsonType],
    ) -> list:
        field_bool = field_list.pop_bool()
        if not field_bool:
            return []
        datalen = data_list.popleft()
        if not isinstance(datalen, int):
            err = f"Expected integer for oject length encoding, instead found {type(datalen)}"
            raise TypeError(err)
        sub_type = var_schema.get("items")
        if not isinstance(sub_type, dict):
            sub_type = None
        return [
            self.deserialize_var(sub_type, schema_defs, field_list, data_list)
            for _ in range(datalen)
        ]

    def deserialize_object(
        self,
        var_schema: dict[str, PyJsonType],
        schema_defs: dict[str, dict],
        field_list: BinaryIterator,
        data_list: deque[PyJsonType],
    ) -> dict:
        field_bool = field_list.pop_bool()
        if not field_bool:
            return {}
        data = {}
        sub_type = var_schema.get("additionalProperties")
        if not isinstance(sub_type, dict):
            sub_type = None
        datalen = data_list.popleft()
        if not isinstance(datalen, int):
            err = f"Expected integer for oject length encoding, instead found {type(datalen)}"
            raise TypeError(err)
        for _ in range(datalen):
            key = self.deserialize_var(None, schema_defs, field_list, data_list)
            data[key] = self.deserialize_var(sub_type, schema_defs, field_list, data_list)
        return data

import itertools
from dataclasses import dataclass, fields
from datetime import date, datetime
from decimal import InvalidOperation
from types import NoneType, UnionType
from typing import (
    Any,
    Callable,
    Self,
    TypeVar,
    Union,
    get_args,
    get_origin,
)

T = TypeVar("T")


class DeserializationError(Exception):
    pass


class SquareReader:
    def __init__(self, data: list[str]):
        self._data = data
        self._pos = 0

    def read(self) -> str:
        if self._pos >= len(self._data):
            return ""

        result = self._data[self._pos]
        self._pos += 1
        return result


class Serializable:
    def to_square(self) -> list[str]:
        raise NotImplementedError()

    @classmethod
    def from_square(cls, reader: SquareReader) -> Self:
        raise NotImplementedError()


@dataclass
class ComplexSerialize(Serializable):
    @classmethod
    def get_serializable_fields(cls) -> list[tuple[str, Any]]:
        fields_to_serialize = []

        for field in fields(cls):
            if "bsqr_order" not in field.metadata:
                continue

            fields_to_serialize.append(
                (field.metadata["bsqr_order"], field.name, field.type)
            )

        fields_to_serialize.sort()
        return [
            (field_name, field_type)
            for _, field_name, field_type in fields_to_serialize
        ]

    def to_square(self) -> list[str]:
        serialized = []
        for field_name, _ in self.get_serializable_fields():
            serialized.extend(serialize_to_square(getattr(self, field_name)))

        return serialized

    @classmethod
    def from_square(cls, reader: SquareReader) -> Self:
        kwargs = {}

        for field_name, field_type in cls.get_serializable_fields():
            try:
                field_value = _deserialize_from_square(reader, field_type)
                kwargs[field_name] = field_value
            except Exception as e:
                raise DeserializationError(f"{field_name}: {e}")

        return cls(**kwargs)


PRIMITIVE_SERIALIZERS: dict[type, Callable[[Any], list[str]]] = {
    date: lambda x: [x.strftime("%Y%m%d")],
    list: lambda x: [str(len(x))]
    + list(itertools.chain.from_iterable([serialize_to_square(i) for i in x])),
    NoneType: lambda _: [""],
}


def _deserialize_list(reader: SquareReader, inside_type: type[T]) -> list[T]:
    length = int(reader.read())
    final = []

    for _ in range(length):
        val = _deserialize_from_square(reader, inside_type)
        final.append(val)

    return final


def _deserialize_none(reader: SquareReader) -> None:
    if reader.read() != "":
        raise ValueError("NoneType with non-empty value")

    return None


PRIMITIVE_DESERIALIZERS: dict[type, Callable[[SquareReader], Any]] = {
    date: lambda reader: datetime.strptime(reader.read(), "%Y%m%d").date(),
    NoneType: _deserialize_none,
}


def serialize_to_square(obj: Any) -> list[str]:
    if isinstance(obj, Serializable):
        return obj.to_square()

    if type(obj) in PRIMITIVE_SERIALIZERS:
        return PRIMITIVE_SERIALIZERS[type(obj)](obj)

    return [str(obj).replace("\t", " ")]


def _deserialize_from_square(reader: SquareReader, type_: Any) -> Any:
    origin = get_origin(type_)
    args = get_args(type_)

    if origin is list:
        return _deserialize_list(reader, args[0])

    if origin in (Union, UnionType):
        for subtype in args:
            pos = reader._pos
            try:
                return _deserialize_from_square(reader, subtype)
            except (TypeError, ValueError, InvalidOperation):
                reader._pos = pos
                continue
        raise ValueError(f"Cannot deserialize union {type_}")

    if isinstance(type_, type) and issubclass(type_, Serializable):
        return type_.from_square(reader)

    if type_ in PRIMITIVE_DESERIALIZERS:
        return PRIMITIVE_DESERIALIZERS[type_](reader)

    return type_(reader.read().strip())


def deserialize_from_square(data: list[str], type_: Any) -> Any:
    try:
        reader = SquareReader(data)
        return _deserialize_from_square(reader, type_)
    except (IndexError, ValueError, TypeError, DeserializationError) as e:
        raise DeserializationError(f"Failed to deserialize {type_}: {e}") from e

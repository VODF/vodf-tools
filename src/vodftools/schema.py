#!/usr/bin/env python3

"""
Elements to build a FITS-compliant schema. This file defines a meta-schema
for FITS bintables and headers.
"""


from pydantic import BaseModel
from enum import Enum, auto

__all__ = [
    "Header",
    "HeaderGroup",
    "Extension",
    "Table",
    "Column",
    "ColumnGroup",
]


class ValueType(str, Enum):
    none = ""
    float64 = "float64"
    float32 = "float32"
    int32 = "int32"
    int16 = "int16"
    char = "char"


class SchemaElement(BaseModel):
    description: str
    required: bool = True


class Header(SchemaElement):
    """A metadata key-value pair"""

    key: str
    dtype: ValueType | None = None
    unit: str = ""


class HeaderGroup(SchemaElement):
    """Group of metadata keywords, with a common description"""

    headers: list[Header]


class Extension(SchemaElement):
    """An HDU in FITS terminology"""

    name: str
    headers: list[Header | HeaderGroup]


class Column(SchemaElement):
    """Column of a Table"""

    name: str
    dtype: ValueType
    ndims: int = 0
    unit: str = ""
    ucd: str = ""
    format: str = None
    required: bool = False


class ColumnGroup(SchemaElement):
    """Group of logically-related columns with their description"""

    columns: list[Column]


class Table(Extension):
    """A FITS BINTable extension"""

    columns: list[Column | ColumnGroup]

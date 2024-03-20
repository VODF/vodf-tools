#!/usr/bin/env python3

"""
Elements to build a FITS-compliant schema. This file defines a meta-schema
for FITS bintables and headers.
"""


from pydantic import BaseModel, validator
from enum import Enum, auto
from typing import Optional

from astropy.io.votable.ucd import check_ucd
from astropy.units import Unit

__all__ = [
    "Header",
    "HeaderGroup",
    "Extension",
    "TableExtension",
    "Column",
    "ColumnGroup",
    "FITSFile",
]



class DataType(str, Enum):
    none = ""  # auto()
    float64 = ("float64",)  # auto()
    float32 = "float32"  # auto()
    int64 = "int64"  # auto()
    int32 = "int32"  # auto()
    int16 = "int16"  # auto()
    char = "char"  # auto()
    uint32 = "uint32"  # auto()
    isotime = "isotime"  # auto()


class SchemaElement(BaseModel):
    """Any element in the FITS schema"""

    description: str
    required: bool = True


class Header(SchemaElement):
    """A metadata key-value pair"""

    key: str
    dtype: DataType | None = None
    unit: Optional[str] = ""
    origin: Optional[str] = None  #: who defined this if not VODF
    value: Optional[str] = None  #: for headers that have to have a fixed value.
    ivoa_key: Optional[str] = None


class HeaderGroup(SchemaElement):
    """Group of metadata keywords, with a common description"""

    headers: list[Header]


class Extension(SchemaElement):
    """An HDU in FITS terminology"""

    name: str
    headers: list[Header | HeaderGroup]
    version: str


class Column(SchemaElement):
    """Column of a Table"""

    name: str
    dtype: DataType
    ndims: int = 0
    unit: str = ""
    ucd: str = ""
    format: Optional[str] = None

    @validator("ucd")
    def is_valid_ucd(cls, val):
        assert check_ucd(val, check_controlled_vocabulary=True), "Not a valid UCD"
        return val

    @validator("unit")
    def is_valid_unit(cls, val):
        return Unit(val).to_string()


class ColumnGroup(SchemaElement):
    """Group of logically-related columns with their description"""

    columns: list[Column]


class TableExtension(Extension):
    """A FITS BINTable extension"""

    columns: list[Column | ColumnGroup]


class FITSFile(SchemaElement):
    """A FITS file containing multiple extensions"""

    extensions: list[TableExtension]

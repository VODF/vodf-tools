#!/usr/bin/env python3

"""
Elements to build a FITS-compliant schema. This file defines a meta-schema
for FITS bintables and headers.
"""


from enum import Enum

from astropy.io.votable.ucd import check_ucd
from astropy.units import Unit
from pydantic import BaseModel, field_validator

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
    """allowed column types."""

    none = ""  # auto()
    float64 = ("float64",)  # auto()
    float32 = "float32"  # auto()
    int64 = "int64"  # auto()
    int32 = "int32"  # auto()
    int16 = "int16"  # auto()
    char = "char"  # auto()
    uint32 = "uint32"  # auto()
    isotime = "isotime"  # auto()
    uuid = "uuid"


class SchemaElement(BaseModel):
    """Any element in the FITS schema."""

    description: str
    required: bool = True


class Header(SchemaElement):
    """A metadata key-value pair."""

    key: str
    dtype: DataType | None = None  #: data type
    unit: str | None = ""  #: astropy unit string representation
    origin: str | None = None  #: who defined this keword
    value: str | None = None  #: for headers that have to have a fixed value.
    allowed_values: list[str] = []
    ivoa_key: str | None = None

    @field_validator("unit")
    @classmethod
    def _is_valid_unit(cls, val):
        """Coerce unit into astropy format."""
        return Unit(val).to_string()


class HeaderGroup(SchemaElement):
    """Group of metadata keywords, with a common description."""

    headers: list[Header]


class Extension(SchemaElement):
    """An HDU in FITS terminology."""

    name: str  #: becomes EXTNAME
    headers: list[Header | HeaderGroup]
    version: int = 0  #: used to distinguish between HDUs with same name (EXTVER)
    datamodel: str | None = ""  #: identifier of data model in this HDU (HDUVERS)
    class_name: str | None = None  #: what standard this extension adheres to (HDUCLASS)
    subclass1: str | None = None  #: level-1 hierarchy of this extension, HDUCLAS1
    subclass2: str | None = None  #: level-2 hierarchy of this extension, HDUCLAS2
    subclass3: str | None = None  #: level-3 hierarchy of this extension, HDUCLAS3


class Column(SchemaElement):
    """Column of a Table."""

    name: str
    dtype: DataType
    ndims: int = 0
    unit: str = ""
    ucd: str = ""
    format: str | None = None

    @field_validator("ucd")
    @classmethod
    def _is_valid_ucd(cls, val):
        """Check if valid IVOA UCD."""
        assert check_ucd(val, check_controlled_vocabulary=True), "Not a valid UCD"
        return val

    @field_validator("unit")
    @classmethod
    def _is_valid_unit(cls, val):
        return Unit(val).to_string()


class ColumnGroup(SchemaElement):
    """Group of logically-related columns with their description."""

    columns: list[Column]


class TableExtension(Extension):
    """A FITS BINTable extension."""

    columns: list[Column | ColumnGroup]


class FITSFile(SchemaElement):
    """A FITS file containing multiple extensions."""

    extensions: list[TableExtension]

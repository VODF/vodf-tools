#!/usr/bin/env python3

"""
Elements to build a FITS-compliant schema.

This file defines a meta-schema for FITS bintables and headers.
"""

from enum import StrEnum, auto
from typing import Annotated

from pydantic import BaseModel, Field

from . import vodf_version_id
from .validators import VALID_NAME_REGEXP, Capitalize, ValidUCD, ValidUnit

__all__ = [
    "SchemaElement",
    "Header",
    "HeaderGroup",
    "Extension",
    "TableExtension",
    "Column",
    "ColumnGroup",
    "FITSFile",
    "DataType",
]


class DataType(StrEnum):
    """allowed column types."""

    none = auto()
    float64 = auto()
    float32 = auto()
    int64 = auto()
    int32 = auto()
    int16 = auto()
    char = auto()
    uint32 = auto()
    isotime = auto()
    uuid = auto()


class Origin(StrEnum):
    """Name of reference for keyword definition."""

    fits = "FITS Standard"
    fits_v4 = "FITS Standard, version 4"
    heasarc = "HEASARC"
    ogip = "OGIP"
    vodf = "VODF"
    fits_timerep = "Representations of time coordinates in FITS, A&A 574, A36 (2015)"


class SchemaElement(BaseModel):
    """Any element in the FITS schema."""

    name: str = Field(pattern=VALID_NAME_REGEXP)
    description: str
    required: bool = True


class Header(SchemaElement):
    """A metadata key-value pair."""

    fits_key: Annotated[str, Capitalize, Field(max_length=8)]
    dtype: DataType | None = None  #: data type
    unit: Annotated[str, ValidUnit] | None = None  #: astropy unit string representation
    origin: Origin | None = None  #: who defined this keword
    value: str | None = None  #: for headers that have to have a fixed value.
    allowed_values: list[str] = []
    ivoa_key: str | None = None


class HeaderGroup(SchemaElement):
    """Group of metadata keywords, with a common description."""

    headers: list[Header]


class Extension(SchemaElement):
    """An HDU in FITS terminology."""

    headers: list[Header | HeaderGroup]
    version: int = 0  #: used to distinguish between HDUs with same name (EXTVER)
    datamodel: str | None = (
        vodf_version_id()
    )  #: identifier of data model in this HDU (HDUVERS)
    class_name: str | None = None  #: what standard this extension adheres to (HDUCLASS)
    subclass1: str | None = None  #: level-1 hierarchy of this extension, HDUCLAS1
    subclass2: str | None = None  #: level-2 hierarchy of this extension, HDUCLAS2
    subclass3: str | None = None  #: level-3 hierarchy of this extension, HDUCLAS3
    subclass4: str | None = None  #: level-4 hierarchy of this extension, HDUCLAS4

    def class_info(self) -> list[str]:
        """Return the class info as an array."""
        if not self.class_name:
            return []
        else:
            return [
                self.class_name,
            ] + [
                x
                for x in [
                    self.subclass1,
                    self.subclass2,
                    self.subclass3,
                    self.subclass4,
                ]
                if x
            ]


class Column(SchemaElement):
    """Column of a Table."""

    dtype: DataType
    ndims: int = 0
    unit: Annotated[str, ValidUnit] | None = None  #: astropy unit string representation
    ucd: Annotated[str, ValidUCD] | None = None
    format: str | None = None  #: format for output to text if not default


class ColumnGroup(SchemaElement):
    """Group of logically-related columns with their description."""

    columns: list[Column]


class TableExtension(Extension):
    """A FITS BINTable extension."""

    columns: list[Column | ColumnGroup]


class FITSFile(SchemaElement):
    """A FITS file containing multiple extensions."""

    extensions: list[TableExtension]

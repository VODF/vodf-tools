#!/usr/bin/env python3
#
# TODO: make fits_template methods be outside the class as a visitor pattern
#

import textwrap

from astropy import units as u
from pydantic import BaseModel

from .visitor import Visitor

@Visitor
def fits_template(): pass

__all__ = [
    "fits_template",
    "Header",
    "HeaderGroup",
    "HDU",
    "TableHDU",
    "Column",
    "ColumnGroup",
]


class SchemaElement(BaseModel):
    description: str
    required: bool = True


class Header(SchemaElement):
    key: str
    dtype: str = "E"

class HeaderGroup(SchemaElement):
    headers: list[Header]


@fits_template.generator(Header)
def _(hdr):
    if len(hdr.key) <= 8:
        yield f"{hdr.key.upper():8s} =       / {hdr.description:50s}"
    else:
        yield f"HIERARCH {hdr.key.upper()} = /  {hdr.description:50s}"



@fits_template.generator(HeaderGroup)
def _(grp, **kwargs):
    yield ""
    yield "# ======================================="
    yield f"# {grp.description}"
    yield "# ======================================="

    for header in grp.headers:
        yield from fits_template(header)


class HDU(SchemaElement):
    name: str
    headers: list[Header | HeaderGroup]

@fits_template.generator(HDU)
def _(hdu):
    yield "#" * 70
    yield f"# HDU: {hdu.name}"
    yield "# DESCRIPTION: "
    yield from textwrap.wrap(
        hdu.description,
        initial_indent="#    ",
        subsequent_indent="#    ",
        drop_whitespace=True,
    )
    yield "#" * 70
    yield "XTENSION = BINTABLE"
    yield f"EXTNAME  = {hdu.name} / {hdu.description:.70s}"
    for header in hdu.headers:
        yield from fits_template(header)


class Column(SchemaElement):
    name: str
    dtype: str
    ndims: int = 0
    unit: str = ""
    ucd: str = ""
    required: bool = False

@fits_template.generator(Column)
def _(col):
    yield f"TTYPE# = {col.name} / {col.description:.70s}"
    yield f"TFORM# = {col.dtype}"
    if col.unit:
        yield (
            f"TUNIT# = {u.Unit(col.unit).to_string('fits')} "
            f"/ or any of type '{u.Unit(col.unit).physical_type}'"
        )
    if col.ucd:
        yield f"TUCD#  = {col.ucd}"
    yield ""  # spacer


class ColumnGroup(SchemaElement):
    columns: list[Column]

@fits_template.generator(ColumnGroup)
def _(grp, **kwargs):
    yield ""
    yield "# ---------------------------------------"
    yield f"# {grp.description}"
    yield "# ---------------------------------------"

    for column in grp.columns:
        yield from fits_template(column)


class TableHDU(HDU):
    columns: list[Column | ColumnGroup]

@fits_template.generator(TableHDU)
def _(table, **kwargs):
    yield from fits_template.generators[HDU](table) # bit if a hack to call parent
    yield ""
    yield "# ======================================="
    yield "# Binary Table"
    yield "# ======================================="
    for column in table.columns:
        yield from fits_template(column)

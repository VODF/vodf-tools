#!/usr/bin/env python3
#
# TODO: make fits_template methods be outside the class as a visitor pattern
#

import textwrap

from astropy import units as u
from pydantic import BaseModel

from .visitor import Visitor

fits_template = Visitor()


class SchemaElement(BaseModel):
    description: str
    required: bool = True

class Header(SchemaElement):
    key: str
    dtype: str = "E"


@fits_template.generator(Header):
def _(self, **kwargs):
    if len(self.key) <= 8:
        yield f"{self.key.upper():8s} =       / {self.description:50s}"
    else:
        yield f"HIERARCH {self.key.upper()} = /  {self.description:50s}"


class HeaderGroup(SchemaElement):
    headers: list[Header]

    def fits_template(self, **kwargs):
        yield ""
        yield "# ======================================="
        yield f"# {self.description}"
        yield "# ======================================="

        for header in self.headers:
            yield from header.fits_template()


class HDU(SchemaElement):
    name: str
    headers: list[Header | HeaderGroup]

    def fits_template(self, **kwargs):
        yield "#" * 70
        yield f"# HDU: {self.name}"
        yield "# DESCRIPTION: "
        yield from textwrap.wrap(
            self.description,
            initial_indent="#    ",
            subsequent_indent="#    ",
            drop_whitespace=True,
        )
        yield "#" * 70
        yield "XTENSION = BINTABLE"
        yield f"EXTNAME  = {self.name} / {self.description:.70s}"
        for header in self.headers:
            yield from header.fits_template()


class Column(SchemaElement):
    name: str
    dtype: str
    ndims: int = 0
    unit: str = ""
    ucd: str = ""
    required: bool = False

    def fits_template(self, **kwargs):
        yield f"TTYPE# = {self.name} / {self.description:.70s}"
        yield f"TFORM# = {self.dtype}"
        if self.unit:
            yield (
                f"TUNIT# = {u.Unit(self.unit).to_string('fits')} "
                f"/ or any of type '{u.Unit(self.unit).physical_type}'"
            )
        if self.ucd:
            yield f"TUCD#  = {self.ucd}"
        yield ""  # spacer


class ColumnGroup(SchemaElement):
    columns: list[Column]

    def fits_template(self, **kwargs):
        yield ""
        yield "# ---------------------------------------"
        yield f"# {self.description}"
        yield "# ---------------------------------------"

        for column in self.columns:
            yield from column.fits_template()


class TableHDU(HDU):
    columns: list[Column | ColumnGroup]

    def fits_template(self, **kwargs):
        yield from super().fits_template()
        yield ""
        yield "# ======================================="
        yield "# Binary Table"
        yield "# ======================================="
        for column in self.columns:
            yield from column.fits_template()

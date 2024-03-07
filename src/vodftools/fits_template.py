"""Defines the methods to generate a FITS Template file from a Schema

This follows the Visitor pattern, where each class is decorated with a function
@fits_template.generator(CLASS) that tells it how to convert that class into a
fits template.

The results can be printed as follows, assuming schema is an object from schema.py:

.. code-block: python

    print("\n".join(fits_template(schema)))

"""
import textwrap
from pathlib import Path

from astropy import units as u

from typing import Generator
from .schema import (
    Column,
    ColumnGroup,
    Extension,
    Header,
    HeaderGroup,
    SchemaElement,
    Table,
    ValueType,
)
from .visitor import visitor

__all__ = ["fits_template", "write_fits_template"]


# From : https://archive.stsci.edu/fits/fits_standard/node68.html#3124
# | TFORMn value | Description                     | 8-bit Bytes |
# |--------------+---------------------------------+-------------|
# | L            | Logical                         |           1 |
# | X            | Bit                             |           * |
# | B            | Unsigned byte                   |           1 |
# | I            | 16-bit integer                  |           2 |
# | J            | 32-bit integer                  |           4 |
# | A            | Character                       |           1 |
# | E            | Single precision floating point |           4 |
# | D            | Double precision floating point |           8 |
# | C            | Single precision complex        |           8 |
# | M            | Double precision complex        |          16 |
# | P            | Array Descriptor                |             |

TYPE_TO_FITS = {
    ValueType.float32: "E",
    ValueType.float64: "D",
    ValueType.int32: "J",
    ValueType.int16: "I",
    ValueType.char: "A",
}


@visitor
def fits_template(schema: SchemaElement) -> Generator:
    """
    Function to create a generator for a FITS TPL from a given schema object.

    Parameters
    ----------
    schema: SchemaElement
        input schema

    Returns
    -------
    Generator:
        lines of the TPL file
    """


def write_fits_template(schema: SchemaElement, output_file: Path) -> None:
    """Write a FITS tpl file for the given SchemaElement

    Parameters
    ----------
    schema: SchemaElement
        Input schema
    output_file: str
        Output filename or path
    """
    with Path(output_file).open(mode="w") as out:
        for line in fits_template(schema):
            out.write(line)
            out.write("\n")


#!/usr/bin/env python3
@fits_template.generator(Header)
def _(hdr):
    extra = ""
    if hdr.unit:
        extra += f" [{u.Unit(hdr.unit).to_string('fits')}]"
    if hdr.dtype:
        extra += f" ({TYPE_TO_FITS[hdr.dtype]})"
    if len(hdr.key) <= 8:
        yield f"{hdr.key.upper():8s} =                     /{extra} {hdr.description:50s}"
    else:
        yield f"HIERARCH {hdr.key.upper()} = /{extra} {hdr.description:50s}"


@fits_template.generator(HeaderGroup)
def _(grp, **kwargs):
    yield ""
    yield "/ " + "=" * 78
    yield f"/ {grp.description}"
    yield "/ " + "=" * 78

    for header in grp.headers:
        yield from fits_template(header)


@fits_template.generator(Extension)
def _(hdu):
    yield "/ " + "#" * 78
    yield f"/ HDU: {hdu.name}"
    yield "/ DESCRIPTION: "
    yield from textwrap.wrap(
        hdu.description,
        initial_indent="/    ",
        subsequent_indent="/    ",
        drop_whitespace=True,
    )
    yield "/ " + "#" * 78
    yield "XTENSION = BINTABLE"
    yield f"EXTNAME  = {hdu.name}"
    for header in hdu.headers:
        yield from fits_template(header)


@fits_template.generator(Column)
def _(col):
    yield f"TTYPE# = {col.name:20s} / {col.description:.70s}"
    yield f"TFORM# = {TYPE_TO_FITS[col.dtype]:20s} / {col.dtype.name}"
    if col.unit:
        yield (
            f"TUNIT# = {u.Unit(col.unit).to_string('fits'):20s} "
            f"/ or convertable to '{u.Unit(col.unit).physical_type}'"
        )
    if col.ucd:
        yield f"TUCD#  = {col.ucd:20s}"
    if col.ndims:
        yield f"TDIM#  = {col.ndims:20s}  / {col.ndims}-dimensional array values"
    if col.format:
        yield f"TDISP#  = {col.format:20s}  / display format"
    yield ""  # spacer


@fits_template.generator(ColumnGroup)
def _(grp, **kwargs):
    yield ""
    yield "/ "+"-" * 60
    yield from textwrap.wrap(
        grp.description,
        initial_indent="/    ",
        subsequent_indent="/    ",
        drop_whitespace=True,
    )
    yield "/ "+"-" * 60

    for column in grp.columns:
        yield from fits_template(column)


@fits_template.generator(Table)
def _(table, **kwargs):
    yield from fits_template.generators[Extension](
        table
    )  # bit if a hack to call parent
    yield ""
    yield "/ " + "=" * 78
    yield "/ Binary Table"
    yield "/ " + "=" * 78
    for column in table.columns:
        yield from fits_template(column)

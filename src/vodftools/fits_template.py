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
from itertools import filterfalse

from astropy import units as u

from typing import Generator
from .schema import (
    Column,
    ColumnGroup,
    Extension,
    Header,
    HeaderGroup,
    SchemaElement,
    TableExtension,
    DataType,
    FITSFile,
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
    DataType.float32: "E",
    DataType.float64: "D",
    DataType.int32: "J",
    DataType.int16: "I",
    DataType.int64: "K",
    DataType.char: "A",
    DataType.isotime: "A",
}


def maybe_long_key_value(key, value):
    yield "&' \n".join(
        textwrap.wrap(
            f"'{value}'",
            width=79,
            initial_indent=f"{key} = ",
            subsequent_indent="CONTINUE '",
        )
    )


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
def _(hdr, **kwargs):
    extra = ""
    if hdr.unit:
        extra += f" [{u.Unit(hdr.unit)}]"
    if hdr.dtype:
        extra += f" ({hdr.dtype.name})"
    optional = "(OPTIONAL)" if hdr.required is False else ""

    maybe_value = hdr.value if hdr.value else ""

    if len(hdr.key) <= 8:
        yield f"{hdr.key.upper():8s} = {maybe_value:20}      /{extra} {hdr.description+optional:50s}"
    else:
        yield f"HIERARCH {hdr.key.upper()} = /{extra} {hdr.description+optional:50s}"


@fits_template.generator(HeaderGroup)
def _(grp, **kwargs):
    yield ""
    yield "/ " + "=" * 78
    yield f"/ {grp.description}"
    yield "/ " + "=" * 78

    for header in grp.headers:
        yield from fits_template(header, **kwargs)


@fits_template.generator(Extension)
def _(hdu, **kwargs):
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

    # TODO: add these as Headers in the constructor?
    yield "XTENSION = BINTABLE"
    yield f"EXTNAME  = {hdu.name}"
    yield f"EXTVER  = {hdu.version}"
    yield from maybe_long_key_value("HDUDOC", hdu.description)
    yield f"HDUVER = {hdu.datamodel}"
    if hdu.class_name:
        yield f"HDUCLASS = {hdu.class_name} / type of HDU"
    if hdu.subclass1:
        yield f"HDUCLAS1 = {hdu.subclass1} / subclass level 1"
    if hdu.subclass2:
        yield f"HDUCLAS2 = {hdu.subclass2} / subclass level 2"
    if hdu.subclass3:
        yield f"HDUCLAS2 = {hdu.subclass3} / subclass level 2"

    for header in hdu.headers:
        yield from fits_template(header, **kwargs)


@fits_template.generator(Column)
def _(col, **kwargs):
    optional = f" (OPTIONAL) " if col.required is False else ""
    yield f"TTYPE# = {col.name:20s} / {col.description+optional:.70s}"
    yield f"TFORM# = {TYPE_TO_FITS[col.dtype]:20s} / {col.dtype.name}"
    if col.unit:
        yield (
            f"TUNIT# = {u.Unit(col.unit):fits} "
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
    yield "/ " + "-" * 60
    yield from textwrap.wrap(
        grp.description,
        initial_indent="/    ",
        subsequent_indent="/    ",
        drop_whitespace=True,
    )
    yield "/ " + "-" * 60

    for column in grp.columns:
        yield from fits_template(column, **kwargs)


@fits_template.generator(TableExtension)
def _(table, **kwargs):
    yield from fits_template.generators[Extension](
        table, **kwargs
    )  # bit if a hack to call parent
    yield ""
    yield "/ " + "=" * 78
    yield "/ Binary Table"
    yield "/ " + "=" * 78
    for column in table.columns:
        yield from fits_template(column, **kwargs)


@fits_template.generator(FITSFile)
def _(ffile, **kwargs):
    yield "/ " + "*" * 78
    yield "/ FITS FILE: "
    yield from textwrap.wrap(
        ffile.description,
        initial_indent="/    ",
        subsequent_indent="/    ",
        drop_whitespace=True,
    )
    yield "/ "
    yield "/ EXTENSIONS SUMMARY:"
    for ii, extension in enumerate(ffile.extensions):
        yield f"/  {ii:3d}. {extension.name:20s} [{extension.__class__.__name__}]"
    yield "/ " + "*" * 78
    yield ""

    for extension in ffile.extensions:
        yield from fits_template(extension, **kwargs)
    yield "END"

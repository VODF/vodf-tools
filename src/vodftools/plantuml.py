#!/usr/bin/env python3

"""Conversion of model schemas to PlantUML diagrams."""

from collections.abc import Generator
from dataclasses import dataclass

from .schema import (
    Column,
    Extension,
    Header,
    HeaderGroup,
    SchemaElement,
    TableExtension,
)
from .visitor import Visitor

__all__ = [
    "plantuml",
]


def plantuml(schema: SchemaElement, **kwargs) -> Generator:
    """Convert schema to a plantuml diagram."""
    yield "@startuml"
    yield "skinparam  wrapWidth 200"
    # yield "skinparam dpi 300"
    yield "skinparam defaultFontName Helvetica"

    for cls in plantuml_class(schema, opts=kwargs):
        yield str(cls)

    for rel in plantuml_relationship(schema, opts=kwargs):
        yield str(rel)

    yield "@enduml"


@dataclass
class Relationship:
    from_class: str
    to_class: str
    arrow: str = "*--"

    def __str__(self):
        return f"{self.from_class} {self.arrow} {self.to_class}"


@Visitor
def plantuml_class(schema: SchemaElement) -> Generator:
    """
    Create a generator for PlantUML text from a given schema object.

    Parameters
    ----------
    schema: vodftools.schema.SchemaElement
        input schema

    Returns
    -------
    Generator:
        lines of the plantUML file
    """


@Visitor
def plantuml_relationship(schema: SchemaElement) -> Generator:
    """
    Create a generator for PlantUML text from a given schema object.

    Parameters
    ----------
    schema: vodftools.schema.SchemaElement
        input schema

    Returns
    -------
    Generator:
        lines of the plantUML file
    """


@plantuml_class.generator(SchemaElement)
def _(element, opts):
    yield f"class {element.name} <<{element.__class__.__name__}>>"


@plantuml_class.generator(HeaderGroup)
def _(group, opts):
    for header in group.headers:
        yield from plantuml_class(header, opts)


@plantuml_class.generator(Extension)
def _(ext, opts):
    yield "{"
    yield f"    + **version** = {ext.version}"
    yield f"    + **datamodel** = {ext.datamodel}"
    yield f"    + **class_hierarchy** = {', '.join(ext.class_hierarchy)}"
    yield "}"
    for header in ext.headers:
        yield from plantuml_class(header, opts)


@plantuml_relationship.generator(Extension)
def _(ext, opts):
    for header in ext.headers:
        yield Relationship(from_class=ext.name, to_class=header.name, arrow="o-l-")
        yield from plantuml_relationship(header, opts)


@plantuml_class.generator(TableExtension)
def _(ext: TableExtension, opts):
    for column in ext.columns:
        yield from plantuml_class(column, opts)


@plantuml_class.generator(Column)
def _(col: Column, opts):
    if opts.get("detail", False):
        yield "{"
        for key, value in col.model_dump(exclude_none=True, exclude=["name"]).items():
            yield f"    + **{key}** = {value}"
        yield "}"


@plantuml_relationship.generator(TableExtension)
def _(ext: TableExtension, opts):
    for column in ext.columns:
        yield Relationship(from_class=ext.name, to_class=column.name, arrow="*-r-")


@plantuml_class.generator(Header)
def _(hdr: Header, opts):
    yield "{"
    if opts.get("detail", False):
        for key, value in hdr.model_dump(exclude_none=True, exclude=["name"]).items():
            yield f"    + **{key}** = {value}"
    else:
        yield f"    + fits_key = {hdr.fits_key}"
    yield "}"


@plantuml_relationship.generator(HeaderGroup)
def _(group, opts):
    for header in group.headers:
        yield Relationship(from_class=group.name, to_class=header.name)
        yield from plantuml_relationship(header, opts)

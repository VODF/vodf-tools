#!/usr/bin/env python3

import pytest
import os
from vodftools.models.level1 import event_list_hdu, soi_hdu, event_file
from vodftools.fits_template import fits_template, write_fits_template

schemas_to_test = [
    pytest.param(event_list_hdu, id="event_list"),
    pytest.param(soi_hdu, id="soi_table"),
    pytest.param(event_file, id="event_file"),
]


@pytest.mark.parametrize("schema", schemas_to_test)
def test_convert_schemas(schema):
    """ try to convert schema to a fits template"""
    for line in fits_template(schema):
        print(line)


@pytest.mark.parametrize("schema", schemas_to_test)
def test_write_schemas(schema, tmp_path):
    """ test we can write the schema to a file """

    path = tmp_path / f"test.tpl"
    write_fits_template(schema, tmp_path / path)
    assert path.exists()

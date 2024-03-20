#!/usr/bin/env python3

import pytest
from vodftools.models.level1 import event_list_hdu, soi_hdu
from vodftools.fits_template import fits_template


@pytest.mark.parametrize(
    "schema",
    [
        pytest.param(event_list_hdu, id="eventlist"),
        pytest.param(soi_hdu, id="SOI table"),
    ],
)
def test_convert_schemas(schema):
    for line in fits_template(schema):
        print(line)

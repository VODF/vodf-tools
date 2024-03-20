#!/usr/bin/env python3

import pytest
from vodftools.models.level1 import event_list_hdu, soi_hdu
from vodftools.fits_template import fits_template


@pytest.mark.parametrize("schema", [event_list_hdu, soi_hdu])
def test_convert_classes(schema):
    for line in fits_template(schema):
        print(line)


def test_event_list():
    for line in fits_template(event_list_hdu):
        print(line)

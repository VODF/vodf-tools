#!/usr/bin/env python3

from vodftools.models.level1 import event_list_hdu
from vodftools.fits_template import fits_template

def test_event_list():
    for line in fits_template(event_list_hdu):
        print(line)

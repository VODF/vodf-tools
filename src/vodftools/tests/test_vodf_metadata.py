#!/usr/bin/env python3
import astropy.units as u
from astropy.io import fits

from vodftools.vodf_metadata import earth_location_headers
from vodftools.fits_template import write_fits_template

import pytest


@pytest.mark.xfail
def test_earth_location_validate():
    # some test data to check in astropy.io.FITS data structures
    header = fits.Header(
        [
            fits.Card(keyword="GEOLAT", value=12.6 * u.deg),
            fits.Card(keyword="GEOLON", value=128 * u.deg),
            fits.Card(keyword="ALTITUDE", value=1800 * u.m),
        ]
    )

    # validate the header:

    vodf_validate(header)

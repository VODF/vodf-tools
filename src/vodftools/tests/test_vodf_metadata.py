#!/usr/bin/env python3
import astropy.units as u
from astropy.io import fits

from vodftools.vodf_metadata import earth_location_headers
from vodftools.fits_template import write_fits_template


def test_earth_location_to_template():
    write_fits_template(earth_location_headers, "earth.tpl")


def test_earth_location_validate():
    # some test data to check
    header = fits.Header(
        [
            fits.Card(keyword="GEOLAT", value=12.6 * u.deg),
            fits.Card(keyword="GEOLON", value=128 * u.deg),
            fits.Card(keyword="ALTITUDE", value=1800 * u.m),
        ]
    )

    # validate the header:

    vodf_validate(header)

#!/usr/bin/env python3
import astropy.units as u
from astropy.io import fits

from vodftools.vodf_metadata import earth_location


def test_earth_location():

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

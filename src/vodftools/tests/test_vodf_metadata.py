#!/usr/bin/env python3
import pytest


@pytest.mark.xfail()
def test_earth_location_validate():
    pass
    # some test data to check in astropy.io.FITS data structures
    # header = fits.Header(
    #     [
    #         fits.Card(keyword="GEOLAT", value=12.6 * u.deg),
    #         fits.Card(keyword="GEOLON", value=128 * u.deg),
    #         fits.Card(keyword="ALTITUDE", value=1800 * u.m),
    #     ]
    # )

    # validate the header:

    # vodf_validate(header)

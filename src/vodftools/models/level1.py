#!/usr/bin/env python3
# licensed under a 3-clause BSD style license - see LICENSE.rst
"""
Level 1 Data Model
==================

Names: Event Data, Science-Ready Data (TODO: choose good name)
CTAO: DL3


 - EVENT
   - EventList
   - GTI
   - SOI
 - Service:
   - IRFs linked
   - ObsTable
 - MONITORING


Useful links:
- https://heasarc.gsfc.nasa.gov/docs/fcg/common_dict.html
- https://fits.gsfc.nasa.gov/standard40/fits_standard40aa-le.pdf

"""


from inspect import iscode
from vodftools.schema import (
    FITSFile,
    Extension,
    Column,
    ColumnGroup,
    HeaderGroup,
    Header,
    DataType,
)

from .metadata import creator_headers, observation_headers, time_headers, earth_location_headers

event_list = Extension(
    description="VODF Level 1 Event List",
    name="EVENTS",
    headers=[
        creator_headers,
        observation_headers,
        time_headers,
        earth_location_headers,
    ],
)

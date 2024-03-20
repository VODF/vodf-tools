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


from .. import vodf_version_id
from vodftools.schema import (
    FITSFile,
    Extension,
    Column,
    ColumnGroup,
    HeaderGroup,
    Header,
    DataType,
    TableExtension,
)

from .metadata import (
    creator_headers,
    observation_headers,
    time_headers,
    earth_location_headers,
    bibliographic_headers,
    space_headers,
)

event_list_hdu = Extension(
    name="EVENTS",
    class_name="OGIP",
    subclass1="EVENTS",
    description="VODF Level 1 Event List",
    datamodel=vodf_version_id(),
    headers=[
        creator_headers,
        bibliographic_headers,
        time_headers,
        space_headers,
        observation_headers,
        earth_location_headers,
    ],
)


time_interval_columns = ColumnGroup(
    description="Defines a time interval",
    columns=[
        Column(
            name="START",
            dtype=DataType.float32,
            description="start of time interval in the timesys",
            unit="u.s",
            ucd="time.start",
            required=True,
        ),
        Column(
            name="STOP",
            dtype=DataType.float32,
            unit="u.s",
            ucd="time.end",
            description="end of time interval in the timesys",
            required=True,
        ),
    ],
)


soi_hdu = TableExtension(
    description="Stable Observation Intervals and their connection to IRFs",
    name="SOI",
    headers=[creator_headers, time_headers,  bibliographic_headers],
    columns=[
        time_interval_columns,
        Column(name="IRF", description="associated IRF", dtype=DataType.char),
    ],
)

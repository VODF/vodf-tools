#!/usr/bin/env python3
# licensed under a 3-clause BSD style license - see LICENSE.rst
"""Level 1 Data Model."""

# - EVENT
#   - event-list table
#   - GTI table
#   - SOI table
# - SERVICE:
#   - IRFs
#   - ObsTable
# - MONITORING (time-series)
#   - data quality
#   - pointing

# Note: GADF Extension info:
#   https://gamma-astro-data-formats.readthedocs.io/en/v0.3/general/hduclass.html


from .. import vodf_version_id
from ..schema import (
    Column,
    ColumnGroup,
    DataType,
    FITSFile,
    TableExtension,
)
from .metadata import (
    bibliographic_headers,
    creator_headers,
    earth_location_headers,
    observation_headers,
    space_headers,
    time_headers,
)

__all__ = ["event_file", "irf_file"]

event_list_hdu = TableExtension(
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
    columns=[],
)


time_interval_columns = ColumnGroup(
    description="Defines a time interval",
    columns=[
        Column(
            name="START",
            dtype=DataType.float32,
            description="start of time interval in the timesys",
            unit="s",
            ucd="time.start",
            required=True,
        ),
        Column(
            name="STOP",
            dtype=DataType.float32,
            unit="s",
            ucd="time.end",
            description="end of time interval in the timesys",
            required=True,
        ),
    ],
)


soi_hdu = TableExtension(
    description="Stable Observation Intervals and their connection to IRFs",
    name="SOI",
    headers=[creator_headers, time_headers, bibliographic_headers],
    columns=[
        time_interval_columns,
        Column(name="IRF", description="associated IRF", dtype=DataType.char),
    ],
)


event_file = FITSFile(
    description="VODF Level-1 Event Data", extensions=[event_list_hdu, soi_hdu]
)


eff_area_2d_hdu = TableExtension(
    description="Effective Area Response",
    name="EFFECTIVE AREA",
    version=1,
    class_name="VODF",
    subclass1="EFF_AREA",
    subclass2="SPATIAL_NONE",
    subclass3="AEFF_2D",
    headers=[creator_headers, bibliographic_headers],
    columns=[],
)

irf_file = FITSFile(
    description="VODF Level-1 Instrumental Response Functions",
    extensions=[eff_area_2d_hdu],
)

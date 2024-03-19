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


#### Metadata for DL3 EventList:

creator_headers = HeaderGroup(
    description="Creator Information",
    headers=[
        Header(
            key="ORIGIN",
            description="Organization or institution that created this file (e.g. CTAO)",
        ),
        Header(key="CREATOR", description="Name of software used to create this file"),
        Header(key="DATE", description="Date file was created"),
        # TODO: contact name, email, software version, format version
    ],
)

instrument_headers = HeaderGroup(
    description="Instrument Information",
    headers=[
        Header(
            key="TELESCOP",
            description="The name of the facility used for the observation",
            origin="FITS Standard v4",
            ivoa_key="facility_name",
        ),
        Header(
            key="INSTRUME",
            description="The name of the instrument used for the observation",
            origin="FITS Standard v4",
            ivoa_key="instrument_name",
        ),
    ],
)

observation_headers = HeaderGroup(
    description="Observation Information",
    # obs_id, object
    headers=[
        Header(
            key="OBS_ID",
            description="Observation identifier",
            source="NASA Extended Keywords",
            ivoa_key="obs_id",
        ),
        Header(
            key="PROP_ID",
            description="Proposal identifier",
            source="VODF",
            required=False,
        ),
        Header(
            key="DATE-BEG",
            dtype=DataType.isotime,
            description="Human readable start of observation (YYYY-MM-DD HH:MM:SS)",
            source="A&A 574, A36 (2015)",
        ),
        Header(
            key="DATE-END",
            dtype=DataType.isotime,
            description="Human readable end of observations (YYYY-MM-DD HH:MM:SS)",
            source="A&A 574, A36 (2015)",
        ),
    ],
)


# MJDREFI int MJDREFF double TIMEUNIT string TIMESYS string TIMEREF
time_headers = HeaderGroup(
    description=(
        "Definition of the machine-readable time "
        "system used for event times and related headers"
    ),
    headers=[
        Header(
            key="MJDREFI",
            description="integer part of reference time",
            dtype=DataType.int32,
            source="A&A 574, A36 (2015)",
        ),
        Header(  # TODO: do we need this? or just use MJDREF?
            key="MJDREFF",
            description="fractional part of reference time",
            dtype=DataType.float64,
            source="A&A 574, A36 (2015)",
        ),
        Header(
            key="TIMESYS",
            description="Time System",
            dtype=DataType.int32,
            source="A&A 574, A36 (2015)",
        ),
        Header(
            key="TIMEUNIT",
            description="unit used to define times",
            value="s",
            source="A&A 574, A36 (2015)",
        ),
        Header(
            key="TSTART",
            dtype=DataType.float64,
            description="Start time of the data in this HDU in the time system defined above",
            source="A&A 574, A36 (2015)",
        ),
        Header(
            key="TSTOP",
            dtype=DataType.float64,
            description="Stop time of the data in this HDU in the time system defined above",
            source="A&A 574, A36 (2015)",
        ),
    ],
)

# acquisition_headers :  sb_id, ...


earth_location_headers = HeaderGroup(
    description="Earth Location Information of the Observatory",
    headers=[
        Header(key="GEOLON", description="Earth Longitude", unit="deg"),
        Header(key="GEOLAT", description="Earth Latitude", unit="deg"),
        Header(
            key="ALTITUDE",
            description="Altitude above sea level",
            unit="m",
        ),
    ],
)

fixity_headers = HeaderGroup(
    description="Fixity headers to ensure data integrity",
    headers=[
        Header(
            key="DATASUM",
            dtype=DataType.uint32,
            description="checksum of the data in the HDU",
            origin="FITS Standard",
            required=False,
        ),
        Header(
            key="CHECKSUM",
            dtype=DataType.uint32,
            description="checksum of the entire HDU",
            origin="FITS Standard",
        ),
    ],
)


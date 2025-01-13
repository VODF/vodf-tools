#!/usr/bin/env python3
# licensed under a 3-clause BSD style license - see LICENSE.rst
"""
Level 1 Data Model.
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

TODO:
- Provenance?
- add UCDs for metadata

Useful links:
- https://heasarc.gsfc.nasa.gov/docs/fcg/common_dict.html
- FITS standard: https://fits.gsfc.nasa.gov/standard40/fits_standard40aa-le.pdf
- UCDs: https://ivoa.net/documents/UCD1+/20230125/EN-UCDlist-1.5-20230125.pdf



"""


from vodftools.schema import DataType, Header, HeaderGroup, Origin

#### Metadata for DL3 EventList:

creator_headers = HeaderGroup(
    # TODO: check curator info from IVOA
    description="Creator Information",
    headers=[
        Header(
            fits_key="ORIGIN",
            description="Organization or institution responsible for this file (e.g. CTAO)",
            origin=Origin.fits,
        ),
        Header(
            fits_key="CREATOR",
            description="Name of software used to create this file",
            origin=Origin.heasarc,
        ),
        Header(fits_key="DATE", description="Date file was created"),
        Header(
            fits_key="DATAID",
            dtype="uuid",
            ucd="meta.id",
            description="unique id of this data product generated at creation time",
        ),
        # TODO: contact name, email, software version, format version
    ],
)

instrument_headers = HeaderGroup(
    description="Instrument Information",
    headers=[
        Header(
            fits_key="TELESCOP",
            description="The name of the facility used for the observation",
            origin=Origin.fits_v4,
            ivoa_key="facility_name",
        ),
        Header(
            fits_key="INSTRUME",
            description="The name of the instrument used for the observation",
            origin=Origin.fits_v4,
            ivoa_key="instrument_name",
        ),
    ],
)

observation_headers = HeaderGroup(
    description="Observation Information",
    # obs_id, object
    headers=[
        Header(
            fits_key="OBS_ID",
            description="Observation identifier",
            source="NASA Extended Keywords",
            ivoa_key="obs_id",
        ),
        Header(
            fits_key="PROP_ID",
            description="Proposal identifier",
            source="VODF",
            required=False,
        ),
        Header(
            fits_key="DATE-BEG",
            dtype=DataType.isotime,
            description="Human readable start of observation (YYYY-MM-DD HH:MM:SS)",
            source="A&A 574, A36 (2015)",
        ),
        Header(
            fits_key="DATE-END",
            dtype=DataType.isotime,
            description="Human readable end of observations (YYYY-MM-DD HH:MM:SS)",
            source="A&A 574, A36 (2015)",
        ),
        Header(
            fits_key="TSTART",
            dtype=DataType.float64,
            description="Start time of the data in this HDU in the TIMESYS",
            source="A&A 574, A36 (2015)",
        ),
        Header(
            fits_key="TSTOP",
            dtype=DataType.float64,
            description="Stop time of the data in this HDU in the TIMESYS ",
            source="A&A 574, A36 (2015)",
        ),
    ],
)


# MJDREFI int MJDREFF double TIMEUNIT string TIMESYS string TIMEREF
time_headers = HeaderGroup(
    description="Temporal coordinate definitions",
    headers=[
        Header(
            fits_key="MJDREFI",
            description="integer part of reference time",
            dtype=DataType.int32,
            source="A&A 574, A36 (2015)",
        ),
        Header(  # TODO: do we need this? or just use MJDREF?
            fits_key="MJDREFF",
            description="fractional part of reference time",
            dtype=DataType.float64,
            source="A&A 574, A36 (2015)",
        ),
        Header(
            fits_key="TIMESYS",
            description="Time System",
            dtype=DataType.int32,
            source="A&A 574, A36 (2015)",
        ),
        Header(
            fits_key="TIMEUNIT",
            description="unit used to define times",
            value="s",
            source="A&A 574, A36 (2015)",
        ),
    ],
)


space_headers = HeaderGroup(
    description="Spatial Coordinate Definitions",
    headers=[
        Header(
            fits_key="EQUINOX",
            dtype=DataType.float32,
            unit="yr",
            value="2000.0",
            description="Celestial equinox used for positions",
            source="OGIP  HFWG r3",
        ),
        Header(
            fits_key="RADECSYS",
            description="Stellar reference frame used for positions.",
            allowed_values=["ICRS", "FK5"],
            source="OGIP HFWG r3",
        ),
    ],
    # EQUINOX type: float
    #
    # RADECSYS type: string
    #
)

# acquisition_headers :  sb_id, ...


earth_location_headers = HeaderGroup(
    description=(
        "Earth Location of the Observatory, "
        "needed to transform between horizonal and celestial coordinate frames"
    ),
    headers=[
        Header(fits_key="GEOLON", description="Longitude of observatory", unit="deg"),
        Header(fits_key="GEOLAT", description="Latitude of observatory", unit="deg"),
        Header(
            fits_key="ALTITUDE",
            description="Altitude (above sea level) observatory",
            unit="m",
        ),
    ],
)

fixity_headers = HeaderGroup(
    description="Fixity headers to ensure data integrity",
    headers=[
        Header(
            fits_key="DATASUM",
            dtype=DataType.uint32,
            description="checksum of the data in the HDU",
            origin=Origin.fits,
            required=False,
        ),
        Header(
            fits_key="CHECKSUM",
            dtype=DataType.uint32,
            description="checksum of the entire HDU",
            origin=Origin.fits,
        ),
    ],
)

bibliographic_headers = HeaderGroup(
    description="Bibliographic Information",
    headers=[
        Header(
            fits_key="AUTHOR",
            description="Contact 'Name <email>' associated with this data product",
            origin=Origin.fits_v4,
            required=True,
        ),
        Header(
            fits_key="REFERENC",
            description="DOI or bibliographic reference of this data product",
            origin=Origin.fits_v4,
            required=False,
        ),
    ],
)

license_headers = HeaderGroup(
    description="License for this data product",
    headers=[
        Header(
            fits_key="LICENSE",
            description="License for this data product (e.g. CC BY-NC)",
            origin=Origin.vodf,
            required=True,
        ),
        Header(
            fits_key="COPYRIGT",
            description="Copyright owners for this data product",
            origin=Origin.vodf,
            required=False,
        ),
    ],
)

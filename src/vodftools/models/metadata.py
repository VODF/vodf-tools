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


from vodftools.schema import DataType, Header, HeaderGroup, Reference

#### Metadata for DL3 EventList:

creator_headers = HeaderGroup(
    # TODO: check curator info from IVOA
    name="CreatorMeta",
    description="Creator Information",
    headers=[
        Header(
            name="organization",
            fits_key="ORIGIN",
            description="Organization or institution responsible for this file (e.g. CTAO)",
            reference=Reference.fits,
        ),
        Header(
            name="software",
            fits_key="CREATOR",
            description="Name of software used to create this file",
            reference=Reference.heasarc,
        ),
        Header(
            name="creation_date", fits_key="DATE", description="Date file was created"
        ),
        Header(
            name="data_product_id",
            fits_key="DATAID",
            dtype="uuid",
            ucd="meta.id",
            description="unique id of this data product generated at creation time",
        ),
        # TODO: contact name, email, software version, format version
    ],
)

instrument_headers = HeaderGroup(
    name="InstrumentMeta",
    description="Instrument Information",
    headers=[
        Header(
            name="facility_name",
            fits_key="TELESCOP",
            description="The name of the facility used for the observation",
            reference=Reference.fits_v4,
            ivoa_key="facility_name",
        ),
        Header(
            name="instrument_name",
            fits_key="INSTRUME",
            description="The name of the instrument used for the observation",
            reference=Reference.fits_v4,
            ivoa_key="instrument_name",
        ),
    ],
)

observation_headers = HeaderGroup(
    name="ObservationMeta",
    description="Observation Information",
    # obs_id, object
    headers=[
        Header(
            name="obs_id",
            fits_key="OBS_ID",
            description="Observation identifier",
            source="NASA Extended Keywords",
            ivoa_key="obs_id",
        ),
        Header(
            name="proposal_id",
            fits_key="PROP_ID",
            description="Proposal identifier",
            source="VODF",
            required=False,
        ),
        Header(
            name="start_date",
            fits_key="DATE-BEG",
            dtype=DataType.isotime,
            description="Human readable start of observation (YYYY-MM-DD HH:MM:SS)",
            source=Reference.fits_timerep,
        ),
        Header(
            name="end_date",
            fits_key="DATE-END",
            dtype=DataType.isotime,
            description="Human readable end of observations (YYYY-MM-DD HH:MM:SS)",
            source=Reference.fits_timerep,
        ),
        Header(
            name="start_time",
            fits_key="TSTART",
            dtype=DataType.float64,
            description="Start time of the data in this HDU in the TIMESYS",
            source=Reference.fits_timerep,
        ),
        Header(
            name="end_time",
            fits_key="TSTOP",
            dtype=DataType.float64,
            description="Stop time of the data in this HDU in the TIMESYS ",
            source=Reference.fits_timerep,
        ),
    ],
)


# MJDREFI int MJDREFF double TIMEUNIT string TIMESYS string TIMEREF
time_headers = HeaderGroup(
    name="TimeMeta",
    description="Temporal coordinate definitions",
    headers=[
        Header(
            name="reference_time_integer",
            fits_key="MJDREFI",
            description="integer part of reference time",
            unit="yr",
            dtype=DataType.int32,
            source=Reference.fits_timerep,
        ),
        Header(  # TODO: do we need this? or just use MJDREF?
            name="reference_time_fraction",
            fits_key="MJDREFF",
            unit="yr",
            description="fractional part of reference time",
            dtype=DataType.float64,
            source=Reference.fits_timerep,
        ),
        Header(
            name="time_system",
            fits_key="TIMESYS",
            description="Time System",
            dtype=DataType.int32,
            source=Reference.fits_timerep,
        ),
        Header(
            name="time_unit",
            fits_key="TIMEUNIT",
            description="unit used to define times",
            value="s",
            source=Reference.fits_timerep,
        ),
    ],
)


space_headers = HeaderGroup(
    name="SpaceMeta",
    description="Spatial Coordinate Definitions",
    headers=[
        Header(
            name="equinox",
            fits_key="EQUINOX",
            dtype=DataType.float32,
            unit="yr",
            value="2000.0",
            description="Celestial equinox used for positions",
            source="OGIP  HFWG r3",
        ),
        Header(
            name="reference_frame",
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
    name="EarthLocation",
    description=(
        "Earth Location of the Observatory, "
        "needed to transform between horizonal and celestial coordinate frames"
    ),
    headers=[
        Header(
            name="observatory_longitude",
            fits_key="GEOLON",
            description="Longitude of observatory",
            unit="deg",
        ),
        Header(
            name="observatory_latitude",
            fits_key="GEOLAT",
            description="Latitude of observatory",
            unit="deg",
        ),
        Header(
            name="observtory_altitude",
            fits_key="ALTITUDE",
            description="Altitude (above sea level) observatory",
            unit="m",
        ),
    ],
)

fixity_headers = HeaderGroup(
    name="Fixity",
    description="Fixity headers to ensure data integrity",
    headers=[
        Header(
            name="data_checksum",
            fits_key="DATASUM",
            dtype=DataType.uint32,
            description="checksum of the data in the HDU",
            reference=Reference.fits,
            required=False,
        ),
        Header(
            name="hdu_checksum",
            fits_key="CHECKSUM",
            dtype=DataType.uint32,
            description="checksum of the entire HDU",
            reference=Reference.fits,
        ),
    ],
)

bibliographic_headers = HeaderGroup(
    name="BibliographyMeta",
    description="Bibliographic Information",
    headers=[
        Header(
            name="author",
            fits_key="AUTHOR",
            description="Contact 'Name <email>' associated with this data product",
            reference=Reference.fits_v4,
            required=True,
        ),
        Header(
            name="reference_doi",
            fits_key="REFERENC",
            description="DOI or bibliographic reference of this data product",
            reference=Reference.fits_v4,
            required=False,
        ),
    ],
)

license_headers = HeaderGroup(
    name="LicenseMeta",
    description="License for this data product",
    headers=[
        Header(
            name="license_type",
            fits_key="LICENSE",
            description="License for this data product (e.g. CC BY-NC)",
            reference=Reference.vodf,
            required=True,
        ),
        Header(
            name="copyright",
            fits_key="COPYRIGT",
            description="Copyright owners for this data product",
            reference=Reference.vodf,
            required=False,
        ),
    ],
)

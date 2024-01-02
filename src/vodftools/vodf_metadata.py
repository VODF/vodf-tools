#!/usr/bin/env python3
"""
Defines the metadata for VODF files using the metaschemas defined in schema.py
"""

from .schema import HeaderGroup, Header, Table

earth_location_headers = HeaderGroup(
    description="Earth Location Information",
    headers=[
        Header(key="GEOLON", description="Earth Longitude", unit="deg", required=False),
        Header(key="GEOLAT", description="Earth Latitude", unit="deg", required=False),
        Header(
            key="ALTITUDE",
            description="Altitude above sea level",
            unit="m",
            required=False,
        ),
    ],
)


event_list = Table(
    name="EVENTS", description="Event List", headers=[earth_location_headers,]
)

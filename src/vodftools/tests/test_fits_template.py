#!/usr/bin/env python3
from vodftools.fits_template import write_fits_template
from vodftools.schema import (
    Column,
    ColumnGroup,
    DataType,
    FITSFile,
    Header,
    HeaderGroup,
    TableExtension,
)


def test_write_complex_template(tmp_path):
    """
    Generate a FITSFile containing multiple HDUs with different headers,
    etc, and ensure it can be converted to a fits template.
    """
    h = Header(
        name="test",
        fits_key="BOOP",
        description="Things",
        dtype=DataType.float32,
        unit="PeV",
    )

    location_headers = HeaderGroup(
        name="Location",
        description="Earth Location Information",
        headers=[
            Header(
                name="geo_lon",
                fits_key="GEOLON",
                description="Earth Longitude",
                unit="deg",
                required=False,
            ),
            Header(
                name="geo_lat",
                fits_key="GEOLAT",
                description="Earth Latitude",
                unit="deg",
                required=False,
            ),
            Header(
                name="alt",
                fits_key="ALTITUDE",
                description="Altitude above sea level",
                unit="m",
                required=False,
            ),
        ],
    )

    t = TableExtension(
        name="EVENTS",
        headers=[h, location_headers],
        datamodel="VODF-test",
        class_hierarchy=["OGIP", "EVENTS", "ALL"],
        description=(
            "Describes an Event List generated by some thingy. "
            "Here is some long text about it that should render correctly even"
            "though the description is quite long."
        ),
        columns=[
            Column(
                name="event_id",
                description="event identifier",
                dtype="float64",
                ndims=0,
            ),
            Column(
                name="energy",
                description="reconstructed energy",
                dtype="float32",
                ndims=0,
                unit="TeV",
                ucd="phys.energy",
            ),
            ColumnGroup(
                name="fov_cols",
                description="Columns Related to the FOV",
                columns=[
                    Column(
                        name="fov_x",
                        description="x position relative to center of FOV",
                        dtype="float64",
                        unit="deg",
                    ),
                    Column(
                        name="fov_y",
                        description="y position relative to center of FOV",
                        dtype="float64",
                        unit="deg",
                    ),
                ],
            ),
        ],
    )

    f = FITSFile(name="test_file", extensions=[t, t, t], description="A Nice FITS file")
    write_fits_template(f, tmp_path / "test.tpl")

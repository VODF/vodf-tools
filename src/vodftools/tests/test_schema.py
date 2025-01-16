import pytest
from pydantic import ValidationError

from vodftools.schema import Column, ColumnGroup


def test_columns_and_groups():
    c1 = Column(
        name="energy",
        description="gamma ray energy (reconstructed)",
        ucd="phys.energy;em.gamma",
        unit="TeV",
        dtype="float32",
    )

    c2 = Column(
        name="time",
        description="gamma ray arrival time",
        ucd="time.epoch",
        unit="s",
        dtype="float64",
    )

    cols = ColumnGroup(name="group", columns=[c1, c2], description="A group of columns")

    assert c1 in cols.columns

    # should fail since ucd is not valid
    with pytest.raises(ValidationError):
        _ = Column(
            name="time",
            description="gamma ray arrival time",
            ucd="some-invalid-name",
            unit="s",
            dtype="float64",
        )

    # should fail since unit is not valid
    with pytest.raises(ValidationError):
        _ = Column(
            name="time",
            description="gamma ray arrival time",
            unit="invalid-unit",
            dtype="float64",
        )

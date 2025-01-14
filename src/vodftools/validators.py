#!/usr/bin/env python3

"""Functions for validating inputs."""

from astropy.io.votable.ucd import check_ucd
from astropy.units import PhysicalType, Unit
from astropy.units.physical import get_physical_type
from pydantic import AfterValidator

__all__ = [
    "ValidUCD",
    "ValidUCD",
    "ValidPhysicalType",
    "Capitalize",
    "VALID_NAME_REGEXP",
]


def valid_ucd(val):
    """Check if valid IVOA UCD."""
    assert check_ucd(val, check_controlled_vocabulary=True), "Not a valid UCD"
    return val


def valid_unit(val):
    """Check if valid unit."""
    return Unit(val).to_string()


def valid_physical_type(physical_type: str | PhysicalType):
    return get_physical_type(physical_type)


VALID_NAME_REGEXP = "^[a-zA-Z_][a-zA-Z0-9_]*$"
ValidUCD = AfterValidator(valid_ucd)
ValidPhysicalType = AfterValidator(valid_physical_type)
ValidUnit = AfterValidator(valid_unit)
Capitalize = AfterValidator(lambda x: str(x).capitalize())

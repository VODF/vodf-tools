#!/usr/bin/env python3


import pytest
from vodftools.models.level1 import eff_area_2d_hdu, event_list_hdu
from vodftools.plantuml import plantuml

models = [
    pytest.param(event_list_hdu, id="event-list"),
    pytest.param(eff_area_2d_hdu, id="eff-area-2d"),
]


@pytest.mark.parametrize("model", models)
def test_dump_plantuml(model):
    """Convert to plantuml."""

    output = list(plantuml(model))

    assert len(output) > 0

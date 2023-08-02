from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

import gdsfactory as gf
from gdsfactory.difftest import difftest

if TYPE_CHECKING:
    from pytest_regressions.data_regression import DataRegressionFixture

    from gdsfactory.component import Component


def add_pads0() -> Component:
    c = gf.components.straight_heater_metal(length=100.0)
    return gf.routing.add_pads_top(component=c, port_names=("l_e1",))


components = [add_pads0]


@pytest.fixture(params=components)
def component(request) -> Component:
    return request.param()


def test_gds(component: Component) -> None:
    """Avoid regressions in GDS geometry shapes and layers."""
    difftest(component)


def test_settings(component: Component, data_regression: DataRegressionFixture) -> None:
    """Avoid regressions when exporting settings."""
    data_regression.check(component.to_dict())


if __name__ == "__main__":
    c = gf.components.straight_heater_metal(length=100.0)
    c = gf.routing.add_pads_top(component=c, port_names=("l_e1",))
    c.show(show_ports=True)

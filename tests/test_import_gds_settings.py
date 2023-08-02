from __future__ import annotations

from typing import Any

from gdsfactory.components import cells

skip_test = {
    "version_stamp",
    "extend_ports_list",
    "extend_port",
    "grating_coupler_tree",
    "compensation_path",
    "spiral_inner_io_with_gratings",
    "component_sequence",
    "straight_heater_metal_90_90",
    "straight_heater_metal_undercut_90_90",
    "mzi_phase_shifter_top_heater_metal",
}

components_to_test = set(cells.keys()) - skip_test


def tuplify(iterable: list | dict) -> Any:
    """From a list or tuple returns a tuple."""
    if isinstance(iterable, list):
        return tuple(map(tuplify, iterable))
    if isinstance(iterable, dict):
        return {k: tuplify(v) for k, v in iterable.items()}
    return iterable


def sort_dict(d: dict[str, Any]) -> dict[str, Any]:
    return {k: d[k] for k in sorted(d)}


# @pytest.mark.parametrize("component_type", components_to_test)
# def test_properties_components(component_type: str) -> Component:
#     """Write component to GDS with settings written on a label.
#     Then import the GDS and check that the settings imported match the original settings.
#     """


pass

"""Straight waveguide."""
from __future__ import annotations

from typing import TYPE_CHECKING

import gdsfactory as gf
from gdsfactory.add_padding import get_padding_points
from gdsfactory.component import Component
from gdsfactory.route_info import route_info_from_cs

if TYPE_CHECKING:
    from gdsfactory.typings import CrossSectionSpec


@gf.cell
def straight(
    length: float = 10.0,
    npoints: int = 2,
    with_bbox: bool = True,
    cross_section: CrossSectionSpec = "strip",
    **kwargs,
) -> Component:
    """Returns a Straight waveguide.

    Args:
    ----
        length: straight length (um).
        npoints: number of points.
        with_bbox: box in bbox_layers and bbox_offsets to avoid DRC sharp edges.
        cross_section: specification (CrossSection, string, CrossSectionFactory dict).
        kwargs: cross_section settings.

    .. code::

        o1 -------------- o2
                length
    """
    p = gf.path.straight(length=length, npoints=npoints)
    x = gf.get_cross_section(cross_section, **kwargs)

    c = Component()
    path = p.extrude(x)
    ref = c << path
    c.add_ports(ref.ports)
    c.info["length"] = length
    c.info["width"] = x.width
    c.info["cross_section"] = cross_section

    c.info["route_info"] = route_info_from_cs(x, length=length)

    if x.info:
        c.info.update(x.info)

    if with_bbox and length and x.bbox_layers:
        padding = []
        for offset in x.bbox_offsets:
            points = get_padding_points(
                component=c,
                default=0,
                bottom=offset,
                top=offset,
            )
            padding.append(points)

        for layer, points in zip(x.bbox_layers, padding):
            c.add_polygon(points, layer=layer)
    c.absorb(ref)
    return c


if __name__ == "__main__":
    nm = 1e-3
    xs = gf.cross_section.strip()
    c = straight()
    print(c.settings.info["settings"]["add_pins"])

    c.show(show_ports=True)

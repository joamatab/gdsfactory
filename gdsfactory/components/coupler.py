from __future__ import annotations

from typing import TYPE_CHECKING

import gdsfactory as gf
from gdsfactory.component import Component
from gdsfactory.components.coupler_straight import (
    coupler_straight as coupler_straight_function,
)
from gdsfactory.components.coupler_symmetric import (
    coupler_symmetric as coupler_symmetric_function,
)

if TYPE_CHECKING:
    from gdsfactory.typings import ComponentSpec, CrossSectionSpec


@gf.cell
def coupler(
    gap: float = 0.236,
    length: float = 20.0,
    coupler_symmetric: ComponentSpec = coupler_symmetric_function,
    coupler_straight: ComponentSpec = coupler_straight_function,
    dy: float = 4.0,
    dx: float = 10.0,
    cross_section: CrossSectionSpec = "strip",
    **kwargs,
) -> Component:
    r"""Symmetric coupler.

    Args:
    ----
        gap: between straights in um.
        length: of coupling region in um.
        coupler_symmetric: spec for bend coupler.
        coupler_straight: spec for straight coupler.
        dy: port to port vertical spacing in um.
        dx: length of bend in x direction in um.
        cross_section: spec (CrossSection, string or dict).
        kwargs: cross_section settings.

    .. code::

               dx                                 dx
            |------|                           |------|
         o2 ________                           ______o3
                    \                         /           |
                     \        length         /            |
                      ======================= gap         | dy
                     /                       \            |
            ________/                         \_______    |
         o1                                          o4

                        coupler_straight  coupler_symmetric


    """
    length = gf.snap.snap_to_grid(length)
    gap = gf.snap.snap_to_grid(gap, nm=2)
    c = Component()

    sbend = gf.get_component(
        coupler_symmetric,
        gap=gap,
        dy=dy,
        dx=dx,
        cross_section=cross_section,
        **kwargs,
    )

    sr = c << sbend
    sl = c << sbend
    cs = c << gf.get_component(
        coupler_straight,
        length=length,
        gap=gap,
        cross_section=cross_section,
        **kwargs,
    )
    sl.connect("o2", destination=cs.ports["o1"])
    sr.connect("o1", destination=cs.ports["o4"])

    c.add_port("o1", port=sl.ports["o3"])
    c.add_port("o2", port=sl.ports["o4"])
    c.add_port("o3", port=sr.ports["o3"])
    c.add_port("o4", port=sr.ports["o4"])

    c.absorb(sl)
    c.absorb(sr)
    c.absorb(cs)
    c.info["length"] = sbend.info["length"]
    c.info["min_bend_radius"] = sbend.info["min_bend_radius"]
    c.auto_rename_ports()

    x = gf.get_cross_section(cross_section, **kwargs)
    if x.add_bbox:
        c = x.add_bbox(c)
    if x.add_pins:
        c = x.add_pins(c)
    return c


if __name__ == "__main__":
    c = coupler(bbox_offsets=[0.5], bbox_layers=[(111, 0)])
    c.show(show_ports=True)

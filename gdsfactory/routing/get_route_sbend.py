from __future__ import annotations

from typing import TYPE_CHECKING

from gdsfactory.components.bend_s import bend_s
from gdsfactory.typings import Route

if TYPE_CHECKING:
    from gdsfactory.port import Port


def get_route_sbend(port1: Port, port2: Port, **kwargs) -> Route:
    """Returns an Sbend Route to connect two ports.

    Args:
    ----
        port1: start port.
        port2: end port.

    Keyword Args:
    ------------
        npoints: number of points.
        with_cladding_box: square bounding box to avoid DRC errors.
        cross_section: function.
        kwargs: cross_section settings.

    .. plot::
        :include-source:

        import gdsfactory as gf

        c = gf.Component("demo_route_sbend")
        mmi1 = c << gf.components.mmi1x2()
        mmi2 = c << gf.components.mmi1x2()
        mmi2.movex(50)
        mmi2.movey(5)
        route = gf.routing.get_route_sbend(mmi1.ports['o2'], mmi2.ports['o1'])
        c.add(route.references)
        c.show()
        c.plot()

    """
    ysize = port2.center[1] - port1.center[1]
    xsize = port2.center[0] - port1.center[0]
    size = (xsize, ysize)

    bend = bend_s(size=size, **kwargs)

    bend_ref = bend.ref()
    bend_ref.connect(next(iter(bend_ref.ports.keys())), port1)

    orthogonality_error = abs(abs(port1.orientation - port2.orientation) - 180)
    if orthogonality_error > 0.1:
        msg = f"Ports need to have orthogonal orientation {orthogonality_error}\nport1 = {port1.orientation} deg and port2 = {port2.orientation}"
        raise ValueError(
            msg,
        )

    return Route(
        references=[bend_ref],
        length=bend.info["length"],
        ports=(port1, port2),
    )


if __name__ == "__main__":
    #     for i in range(N)
    #     for i in range(N)

    # for p1, p2 in zip(right_ports, left_ports):

    import gdsfactory as gf

    c = gf.Component("demo_route_sbend")
    mmi1 = c << gf.components.mmi1x2()
    mmi2 = c << gf.components.mmi1x2()
    mmi2.movex(50)
    mmi2.movey(5)
    route = gf.routing.get_route_sbend(mmi1.ports["o2"], mmi2.ports["o1"])
    c.add(route.references)
    c.show()

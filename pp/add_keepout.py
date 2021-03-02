from typing import List, Tuple

from phidl.device_layout import _parse_layer

from pp.component import Component
from pp.container import container
from pp.geo_utils import polygon_grow
from pp.layers import LAYER


@container
def add_keepout(
    component: Component,
    target_layers: List[Tuple[int, int]],
    keepout_layers: List[Tuple[int, int]],
    margin: float = 2.0,
) -> Component:
    """Adds keepout after Looking up all polygons in a cell.
    You can also use add_padding

    Args:
        component
        target_layers: list of layers to read
        keepout_layers: list of layers to add keepout
        margin: offset from tareget to keepout_layers
    """
    c = Component(f"{component.name}_ko")
    c << component
    for layer in target_layers:
        polygons = component.get_polygons(by_spec=layer)
        if polygons:
            for ko_layer in keepout_layers:
                ko_layer = _parse_layer(ko_layer)
                polygon_keepout = [
                    polygon_grow(polygon, margin) for polygon in polygons
                ]
                c.add_polygon(polygon_keepout, ko_layer)
    return c


def test_add_keepout() -> None:
    from pp.components.waveguide import waveguide

    c = waveguide()
    polygons = 2
    target_layers = [LAYER.WG]
    keepout_layers = [LAYER.NO_TILE_SI]
    print(len(c.get_polygons()))

    assert len(c.get_polygons()) == polygons
    c = add_keepout(c, target_layers=target_layers, keepout_layers=keepout_layers)
    # print(len(c.get_polygons()))
    assert len(c.get_polygons()) == polygons + 1


if __name__ == "__main__":
    test_add_keepout()

    # import pp
    # from pp.components.crossing_waveguide import crossing_etched
    # from pp.components.crossing_waveguide import crossing45
    # from pp.components.waveguide import waveguide

    # c = crossing45(alpha=0.5, crossing=crossing_etched)
    # c = waveguide()
    # c = pp.c.mzi2x2()

    # target_layers = [LAYER.WG]
    # keepout_layers = [LAYER.SLAB150]
    # c = add_keepout(c, target_layers, keepout_layers)
    # c.show()

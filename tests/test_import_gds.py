from __future__ import annotations

import gdsfactory as gf
from gdsfactory.read.import_gds import import_gds

# def test_import_gds_snap_to_grid() -> None:

#     for polygon in c.get_polygons(by_spec=False):
#         assert gf.snap.is_on_grid(
#             polygon.points, 5
#         ), f"{polygon.points} not in 5nm grid"


def test_import_gds_hierarchy() -> None:
    c0 = gf.components.mzi_arms(delta_length=11)
    gdspath = c0.write_gds()

    c = import_gds(gdspath)
    assert len(c.get_dependencies()) == 3, len(c.get_dependencies())
    assert c.name == c0.name, c.name


# def test_import_gds_add_padding() -> None:


def test_import_gds_array() -> None:
    """Make sure you can import a GDS with arrays."""
    c0 = gf.components.array(
        gf.components.rectangle,
        rows=2,
        columns=2,
        spacing=(10, 10),
    )
    gdspath = c0.write_gds()

    gf.clear_cache()
    c1 = import_gds(gdspath)
    assert len(c1.get_polygons()) == 4


def test_import_gds_raw() -> None:
    """Make sure you can import a GDS with arrays."""
    c0 = gf.components.array(
        gf.components.rectangle,
        rows=2,
        columns=2,
        spacing=(10, 10),
    )
    gdspath = c0.write_gds()

    gf.clear_cache()
    c = gf.read.import_gds(gdspath)
    assert c


if __name__ == "__main__":
    test_import_gds_hierarchy()

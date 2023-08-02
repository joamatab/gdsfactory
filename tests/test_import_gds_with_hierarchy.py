from __future__ import annotations

from typing import TYPE_CHECKING

import jsondiff

import gdsfactory as gf
from gdsfactory.cross_section import cross_section

if TYPE_CHECKING:
    from pytest_regressions.data_regression import DataRegressionFixture

gdspath = gf.PATH.gdsdir / "mzi2x2.gds"


def test_read_gds_hash2() -> None:
    c = gf.import_gds(gdspath)

    h = "2300f7a05e32689af867fb6aa7c6928a711ad474"
    assert c.hash_geometry() == h, f"h = {c.hash_geometry()!r}"


def test_read_gds_with_settings2(data_regression: DataRegressionFixture) -> None:
    c = gf.import_gds(gdspath, read_metadata=True)
    data_regression.check(c.to_dict())


def test_read_gds_equivalent2() -> None:
    """Ensures we can load it from GDS + YAML and get the same component
    settings.
    """
    splitter = gf.components.mmi1x2(cross_section=cross_section)
    c1 = gf.components.mzi(splitter=splitter, cross_section=cross_section)
    c2 = gf.import_gds(gdspath, read_metadata=True)

    d1 = c1.to_dict()
    d2 = c2.to_dict()

    # we change the name, so there is no cache conflicts

    d = jsondiff.diff(d1, d2)

    assert len(d) == 0, d


def test_mix_cells_from_gds_and_from_function2() -> None:
    """Ensures not duplicated cell names.

    when cells loaded from GDS and have the same name as a function with
    @cell decorator

    """
    c = gf.Component("test_mix_cells_from_gds_and_from_function")
    c << gf.components.mzi()
    c << gf.import_gds(gdspath)
    c.write_gds()


def _write() -> None:
    splitter = gf.components.mmi1x2(cross_section=cross_section)
    c1 = gf.components.mzi(splitter=splitter, cross_section=cross_section)
    c1.write_gds(gdspath=gdspath, with_metadata=True)


if __name__ == "__main__":
    _write()
    test_read_gds_equivalent2()

    c = test_read_gds_hash2()

    c1 = gf.components.mzi()
    c2 = gf.import_gds(gdspath)
    d1 = c1.to_dict()
    d2 = c2.to_dict()

    d = jsondiff.diff(d1, d2)
    print(d)

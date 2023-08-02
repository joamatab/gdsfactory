from __future__ import annotations

from functools import partial

import toolz

import gdsfactory as gf

extend_ports1 = partial(gf.components.extend_ports, length=1)
extend_ports2 = partial(gf.components.extend_ports, length=10)


straigth_extended1 = toolz.compose(
    extend_ports1,
    partial(gf.components.straight, width=0.5),
)
straigth_extended2 = toolz.compose(
    extend_ports2,
    partial(gf.components.straight, width=0.9),
)
straigth_extended3 = toolz.compose(
    extend_ports2,
    partial(gf.components.straight, width=0.5),
)


def test_compose1() -> None:
    """Ensures the first level of composed function gets a unique name."""
    extend_ports1 = partial(gf.components.extend_ports, length=1)
    straigth_extended500 = gf.compose(
        extend_ports1,
        partial(gf.components.straight, width=0.5),
    )

    extend_ports2 = partial(gf.components.extend_ports, length=10)
    straigth_extended900 = gf.compose(
        extend_ports2,
        partial(gf.components.straight, width=0.9),
    )

    c500 = straigth_extended500()
    c900 = straigth_extended900()

    assert c900.name != c500.name, f"{c500.name} must be different from {c900.name}"


# def test_compose2():
#     """Ensures the second level of composed function gets a unique name.

#     FIXME! this one does not work

#     """


if __name__ == "__main__":
    test_compose1()

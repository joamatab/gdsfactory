import warnings

import numpy as np

import gdsfactory as gf
from gdsfactory.component import Component
from gdsfactory.components.bend_euler import bend_euler180
from gdsfactory.types import ComponentSpec, CrossSectionSpec


@gf.cell
def delay_snake3(
    length: float = 1600.0,
    length0: float = 0.0,
    n: int = 2,
    bend180: ComponentSpec = bend_euler180,
    cross_section: CrossSectionSpec = "strip",
    **kwargs,
) -> Component:
    r"""Snake input facing west.


    Args:
        length: total length.
        length0: initial offset.
        n: number of loops.
        bend180: ubend spec.
        cross_section: cross_section spec.
        kwargs: cross_section settings.

    .. code::

                 | length0   |

                 >---------\
                            \bend180.info['length']
                            /
       |-------------------/
       |
       |------------------->

       |   delta_length    |


    """
    if n % 2:
        warnings.warn(f"rounding {n} to {n//2 *2}", stacklevel=3)
        n = n // 2 * 2
    bend180 = gf.get_component(bend180, cross_section=cross_section, **kwargs)

    delta_length = (length - length0 - n * bend180.info["length"]) / (n + 1)
    assert (
        delta_length > 0
    ), "Snake is too short: either reduce length0, increase the total length,\
    or decrease n"

    s0 = gf.components.straight(cross_section=cross_section, length=length0, **kwargs)
    sd = gf.components.straight(
        cross_section=cross_section, length=delta_length, **kwargs
    )

    symbol_to_component = {
        "_": (s0, "o1", "o2"),
        "-": (sd, "o1", "o2"),
        ")": (bend180, "o2", "o1"),
        "(": (bend180, "o1", "o2"),
    }

    sequence = "_)" + n // 2 * "-(-)"
    sequence = sequence[:-1]
    c = gf.components.component_sequence(
        sequence=sequence, symbol_to_component=symbol_to_component
    )
    gf.port.auto_rename_ports(c)
    return c


def test_delay_snake3_length() -> Component:
    length = 200.0
    c = delay_snake3(
        n=2,
        length=length,
    )
    length_measured = (
        c.aliases[")1"].parent.info["length"] * 2
        + c.aliases["-1"].parent.info["length"] * 3
    )
    assert np.isclose(
        length, length_measured
    ), f"length measured = {length_measured} != {length}"
    return c


if __name__ == "__main__":
    # c = test_delay_snake3_length()
    length = 200.0
    c = delay_snake3(n=2, length=length, length0=50)
    c.show(show_ports=True)

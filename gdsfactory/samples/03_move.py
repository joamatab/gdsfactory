"""based on phidl tutorial.

# Manipulating geometry 1 - Basic movement and rotation

There are several actions we can take to move and rotate the geometry.
These actions include movement, rotation, and reflection.
"""

from __future__ import annotations

import gdsfactory as gf

if __name__ == "__main__":
    c = gf.Component("demo")

    wg1 = c << gf.components.straight(length=10, width=1)
    wg2 = c << gf.components.straight(length=10, width=2, layer=gf.LAYER.SLAB90)

    # You can play with the following move commands

    c.show(show_ports=True)

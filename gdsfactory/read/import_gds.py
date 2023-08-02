from __future__ import annotations

from pathlib import Path

import gdstk
from omegaconf import OmegaConf

from gdsfactory.cell import Settings, cell
from gdsfactory.component import Component
from gdsfactory.component_reference import ComponentReference
from gdsfactory.config import logger
from gdsfactory.name import get_name_short


@cell
def import_gds(
    gdspath: str | Path,
    cellname: str | None = None,
    gdsdir: str | Path | None = None,
    read_metadata: bool = False,
    hashed_name: bool = True,
    **kwargs,
) -> Component:
    """Returns a Component from a GDS file.

    appends $ with a number to the name if the cell name is on CACHE

    Args:
    ----
        gdspath: path of GDS file.
        cellname: cell of the name to import. None imports top cell.
        gdsdir: optional GDS directory.
        read_metadata: loads metadata (ports, settings) if it exists in YAML format.
        hashed_name: appends a hash to a shortened component name.
        kwargs: extra to add to component.info (polarization, wavelength ...).
    """
    gdspath = Path(gdsdir) / Path(gdspath) if gdsdir else Path(gdspath)
    if not gdspath.exists():
        msg = f"No file {str(gdspath)!r} found"
        raise FileNotFoundError(msg)

    metadata_filepath = gdspath.with_suffix(".yml")

    if gdspath.suffix.lower() == ".gds":
        gdsii_lib = gdstk.read_gds(str(gdspath))
    elif gdspath.suffix.lower() == ".oas":
        gdsii_lib = gdstk.read_oas(str(gdspath))
    else:
        msg = f"gdspath.suffix {gdspath.suffix!r} not .gds or .oas"
        raise ValueError(msg)

    top_level_cells = gdsii_lib.top_level()
    top_cellnames = [c.name for c in top_level_cells]

    if not top_cellnames:
        msg = f"no top cells found in {str(gdspath)!r}"
        raise ValueError(msg)

    D_list = []
    cell_name_to_component = {}
    cell_to_component = {}

    # create a new Component for each gdstk Cell
    for c in gdsii_lib.cells:
        D = Component(name=c.name)
        D._cell = c
        D.name = c.name

        if hashed_name:
            D.name = get_name_short(D.name)

        cell_name_to_component[c.name] = D
        cell_to_component[c] = D
        D_list += [D]

    cellnames = list(cell_name_to_component.keys())
    if cellname is not None:
        if cellname not in cell_name_to_component:
            msg = f"cell {cellname!r} is not in file {gdspath} with cells {cellnames}"
            raise ValueError(
                msg,
            )
    elif len(top_level_cells) == 1:
        cellname = top_level_cells[0].name
    elif len(top_level_cells) > 1:
        msg = f"import_gds() There are multiple top-level cells in {gdspath!r}, you must specify `cellname` to select of one of them among {cellnames}"
        raise ValueError(
            msg,
        )

    # create a new ComponentReference for each gdstk CellReference
    for c, D in cell_to_component.items():
        for e in c.references:
            ref_device = cell_to_component[e.cell]
            ref = ComponentReference(
                component=ref_device,
                origin=e.origin,
                rotation=e.rotation,
                magnification=e.magnification,
                x_reflection=e.x_reflection,
                columns=e.repetition.columns or 1,
                rows=e.repetition.rows or 1,
                spacing=e.repetition.spacing,
                v1=e.repetition.v1,
                v2=e.repetition.v2,
            )
            D._register_reference(ref)
            D._references.append(ref)
            ref._reference = e

    component = cell_name_to_component[cellname]

    if read_metadata and metadata_filepath.exists():
        logger.info(f"Read YAML metadata from {metadata_filepath}")
        metadata = OmegaConf.load(metadata_filepath)

        if "settings" in metadata:
            settings = OmegaConf.to_container(metadata.settings)
            if settings:
                component.settings = Settings(**settings)

        if "ports" in metadata:
            for port_name, port in metadata.ports.items():
                if port_name not in component.ports:
                    component.add_port(
                        name=port_name,
                        center=port.center,
                        width=port.width,
                        orientation=port.orientation,
                        layer=tuple(port.layer),
                        port_type=port.port_type,
                    )

    component.info.update(**kwargs)
    component.imported_gds = True
    return component


def import_gds_raw(gdspath, top_cellname: str | None = None):
    if not top_cellname:
        if gdspath.suffix.lower() == ".gds":
            gdsii_lib = gdstk.read_gds(str(gdspath))
        elif gdspath.suffix.lower() == ".oas":
            gdsii_lib = gdstk.read_oas(str(gdspath))
        top_level_cells = gdsii_lib.top_level()
        top_cellnames = [c.name for c in top_level_cells]
        top_cellname = top_cellnames[0]

    cells = gdstk.read_rawcells(gdspath)
    c = Component(name=top_cellname)
    c._cell = cells.pop(top_cellname)
    return c


if __name__ == "__main__":
    import gdsfactory as gf

    c = gf.components.array()
    gdspath = c.write_gds()

    gf.clear_cache()
    c = import_gds(gdspath)
    c.show(show_ports=False)

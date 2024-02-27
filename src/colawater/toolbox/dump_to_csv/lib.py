from pathlib import Path
from typing import Any

import arcpy

from colawater.lib import layer as ly
from colawater.lib.error import fallible


@fallible
def dump_to_csv(input_layers: list[Any], dest_dir: Path) -> list[Path]:
    """
    Dump attribute table of layers in input_layers to CSVs in dest_dir.

    Arguments:
        input_layers (list[Any]): List of input items supported by Export Table.
                                  (These types are private in ArcPy or hard-to-find, hence the ``Any`` annotation)
        dest_dir (Path): Destination directory for exported files.

    Returns:
        list[Path]: List of paths to the exported files.
    """
    outputs = [
        dest_dir / f"{name}.csv" for name in (ly.name(layer) for layer in input_layers)
    ]

    for layer, dest in zip(input_layers, outputs):
        arcpy.conversion.ExportTable(  # pyright: ignore [reportGeneralTypeIssues]
            layer, str(dest)
        )

    return outputs

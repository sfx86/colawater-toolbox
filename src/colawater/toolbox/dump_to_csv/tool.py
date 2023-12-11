"""
Contains the functions used by the Dump to CSV
tool and other helper functions.
"""

from pathlib import Path
from typing import Any, List

import arcpy

import colawater.lib.layer as ly
from colawater.lib.error import fallible
from colawater.lib.progressor import progressor


@progressor("Dumping layers to CSV...")
def execute(parameters: list[arcpy.Parameter]) -> None:
    """
    Entry point for Dump to CSV.

    Dumps full attribute tables of input layers to CSV files in the target directory.

    Arguments:
        parameters (list[arcpy.Parameter]): The list of parameters.
    """
    input_layers = parameters[0].values
    dest_dir = Path(parameters[1].valueAsText).resolve()

    dump_to_csv(input_layers, dest_dir)


def parameters() -> list[arcpy.Parameter]:
    """
    Returns the parameters for Dump to CSV.

    Parameters are of type GPFeatureLayer multivalue and DEFolder.

    Returns:
        list[arcpy.Parameter]: The list of parameters.
    """
    input_layers = arcpy.Parameter(
        displayName="Input Layers",
        name="input_layers",
        datatype="GPFeatureLayer",
        parameterType="Required",
        direction="Input",
        multiValue=True,
    )
    dest_dir = arcpy.Parameter(
        displayName="Output Folder",
        name="dest_dir",
        datatype="DEFolder",
        parameterType="Required",
        direction="Input",
    )

    return [input_layers, dest_dir]


@fallible
def dump_to_csv(
    input_layers: List[Any],
    dest_dir: Path,
) -> List[Path]:
    """
    Dump attribute table of layers in input_layers to CSVs in dest_dir.

    Arguments:
        input_layers (List[Any]): List of input items supported by Export Table.
                                  (These types are private in ArcPy or hard-to-find, hence the ``Any`` annotation)
        dest_dir (Path): Destination directory for exported files.

    Returns:
        List[Path]: List of paths to the exported files.
    """
    outputs = [
        dest_dir / f"{name}.csv" for name in (ly.name(layer) for layer in input_layers)
    ]

    for layer, dest in zip(input_layers, outputs):
        arcpy.conversion.ExportTable(  # pyright: ignore [reportGeneralTypeIssues]
            layer, str(dest)
        )

    return outputs

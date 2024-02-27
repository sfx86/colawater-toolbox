"""
Contains the functions used by the Dump to CSV
tool and other helper functions.
"""

from pathlib import Path
from typing import Any

import arcpy

from colawater.lib import tool
from colawater.toolbox.dump_to_csv.lib import dump_to_csv


class DumpToCSV:
    @tool.entry("Dumping layers to CSV...")
    def execute(self, parameters: list[arcpy.Parameter]) -> None:
        """
        Entry point for Dump to CSV.

        Dumps full attribute tables of input layers to CSV files in the target directory.

        Arguments:
            parameters (list[arcpy.Parameter]): The list of parameters.
        """
        input_layers = parameters[0].values
        dest_dir = Path(parameters[1].valueAsText).resolve()

        dump_to_csv(input_layers, dest_dir)

    def parameters(self) -> list[arcpy.Parameter]:
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

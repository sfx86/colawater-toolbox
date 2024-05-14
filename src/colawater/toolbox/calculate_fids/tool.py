"""
Calculate Facility Identifiers
"""

from getpass import getuser
from typing import Any

import arcpy
import arcpy._mp

import colawater.lib.layer as ly
from colawater.lib import desc, tool
from colawater.toolbox.calculate_fids.lib import AssetType, calculate_fids


class CalculateFacIDs:
    category = tool.Category.CheckIn.value
    label = "Calculate Facility Identifiers"
    canRunInBackground = False

    def execute(self, parameters: list[arcpy.Parameter], messages: list[Any]) -> None:
        """
        Entry point for Calculate Facility Identifiers.

        Calculates the new facility identifiers for features with given
        placeholder initials starting from a given start value.

        Arguments:
            parameters (list[arcpy.Parameter]): The list of parameters.
            messages (list[Any]): The list of messages.
        """

        placeholder: str = parameters[0].value
        interval: int = parameters[1].value
        value_table: list[tuple[arcpy._mp.Layer, str, int]] = parameters[2].values

        for layer, asset_type, start in value_table:
            basename = desc.basename(layer)

            if start is None:
                arcpy.AddWarning(f"Start value omitted: skipping [{basename}]")
                continue

            if not ly.has_field(layer, "FACILITYID"):
                arcpy.AddWarning(f"Missing field 'FACILITYID': skipping [{basename}]")

            new_fid = calculate_fids(
                layer,
                AssetType(asset_type),
                placeholder,
                interval,
                start,
            )

            arcpy.AddMessage(
                f"{basename}: {new_fid}"
                if new_fid is not None
                else f"{basename}: None used"
            )

    def getParameterInfo(self) -> list[arcpy.Parameter]:
        """
        Returns the parameters for Calculate Facility Identifiers.

        Parameters are of type GPString, GPLong, GPValueTable[DEFeatureClass, GPString, GPLong] multivalue.

        Returns:
            list[arcpy.Parameter]: The list of parameters.
        """
        placeholder = arcpy.Parameter(
            displayName="Facility Identifier Placeholder",
            name="placeholder",
            datatype="GPString",
            parameterType="Required",
            direction="Input",
        )
        placeholder.value = getuser()[:3].upper()

        interval = arcpy.Parameter(
            displayName="Interval",
            name="interval",
            datatype="GPLong",
            parameterType="Required",
            direction="Input",
        )
        interval.value = 2

        inputs = arcpy.Parameter(
            displayName="Inputs",
            name="inputs",
            datatype="GPValueTable",
            parameterType="Required",
            direction="Input",
            multiValue=True,
        )
        inputs.columns = [
            ["DEFeatureClass", "Feature Class"],
            ["GPString", "Asset Type"],
            ["GPLong", "Start Value"],
        ]
        inputs.filters[1].type = "ValueList"
        inputs.filters[1].list = [variant.value for variant in AssetType]

        return [placeholder, interval, inputs]

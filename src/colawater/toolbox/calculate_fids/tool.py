"""
Calculate Facility Identifiers
"""

from getpass import getuser
from typing import Any

import arcpy
import arcpy.management

import colawater.lib.layer as ly
from colawater.lib import desc, tool

from .lib import AssetType, calculate_fids, guess_asset_type


class CalculateFacilityIdentifiers:
    # category = tool.Category.CheckIn.value
    label = "Calculate Facility Identifiers"
    canRunInBackground = False

    def execute(self, parameters: list[arcpy.Parameter], messages: list[Any]) -> None:
        placeholder: str = parameters[0].value
        interval: int = parameters[1].value
        value_table: list[
            tuple[
                arcpy._mp.Layer,  # pyright: ignore [reportAttributeAccessIssue]
                str,
                int,
            ]
        ] = parameters[2].values

        arcpy.AddMessage("Layer -> Next starting value\n")

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

            arcpy.AddMessage(f"{basename} -> {new_fid}")

    def getParameterInfo(self) -> list[arcpy.Parameter]:
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
            ["GPFeatureLayer", "Feature Class"],
            ["GPString", "Asset Type"],
            ["GPLong", "Start Value"],
        ]
        inputs.filters[1].type = "ValueList"
        inputs.filters[1].list = [variant.value for variant in AssetType]

        return [placeholder, interval, inputs]

    def updateParameters(
        self, parameters: list[arcpy.Parameter]
    ) -> list[arcpy.Parameter]:
        return parameters
        # for item in parameters[2].values:
        #     item[1] = guess_asset_type(item[1])

        # return parameters

    # fmt: off
    def isLicensed(self) -> bool: return True
    def postExecute(self, parameters: list[arcpy.Parameter]) -> None: pass
    def updateMessages(self, parameters: list[arcpy.Parameter]) -> None: pass
    # fmt: on

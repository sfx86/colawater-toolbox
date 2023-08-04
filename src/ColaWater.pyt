from typing import Any

import arcpy

from colawater import tools


class Toolbox:
    """
    Contains metadata about the toolbox and what tools it holds.

    ArcGIS ingests this class and uses it to create the geoprocessing tools' UIs
    and use their functionality by calling known methods on the classes included in
    ``self.tools``.

    Attributes:
        label (str): The toolbox label.
        alias (str): The toolbox alias.
        tools (list[Any]): A list of the tools associated with this toolbox.
    """

    def __init__(self) -> None:
        self.label = "Columbia Water"
        self.alias = "ColaWater"
        self.tools = [
            AppendToART,
            CalculateFacilityIdentifiers,
            WaterQualityControl,
        ]


class CalculateFacilityIdentifiers:
    def __init__(self) -> None:
        self.label = "Calculate Facility Identifiers"
        self.description = "Calculates FIDs and FID indices for specified water layers."
        self.canRunInBackground = False

    def getParameterInfo(self) -> list[arcpy.Parameter]:
        return tools.fid_calculator.parameters()

    def updateParameters(self, parameters: list[arcpy.Parameter]) -> None:
        tools.fid_calculator.update_parameters(parameters)

    def execute(self, parameters: list[arcpy.Parameter], messages: Any) -> None:
        tools.fid_calculator.execute(parameters)


class WaterQualityControl:
    def __init__(self) -> None:
        self.label = "Water Quality Control"
        self.description = (
            "Executes selected quality control checks on specified water layers."
        )
        self.canRunInBackground = False

    def getParameterInfo(self) -> list[arcpy.Parameter]:
        return tools.quality_control.parameters()

    def execute(self, parameters: list[arcpy.Parameter], messages: Any) -> None:
        tools.quality_control.execute(parameters)


class AppendToART:
    def __init__(self) -> None:
        self.label = "Append to ART"
        self.description = "Appends new integrated mains to the Asset Reference Table."
        self.canRunInBackground = False

    def getParameterInfo(self) -> list[arcpy.Parameter]:
        return tools.append_art.parameters()

    def execute(self, parameters: list[arcpy.Parameter], messages: Any) -> None:
        tools.append_art.execute(parameters)

from enum import Enum, unique
from types import ModuleType
from typing import Any, Optional

import arcpy
from toolbox import append_to_art, calculate_fids, quality_control


class Toolbox:
    def __init__(self) -> None:
        self.label = "Columbia Water"
        self.alias = "colawater"
        self.tools = [
            AppendToART,
            CalculateFacilityIdentifiers,
            WaterQualityControl,
        ]


@unique
class ToolCategory(Enum):
    VALIDATION = "Data Validation"
    MUTATION = "Update Layers"


def tool(
    label: str,
    description: str,
    category: ToolCategory,
    backgroundable: bool,
    module: ModuleType,
) -> type:
    def module_has_function(name: str) -> bool:
        return callable(getattr(module, name, None))

    class Tool:
        def __init__(self) -> None:
            self.label = label
            self.description = description
            self.category = category.value
            self.canRunInBackground = backgroundable

        if module_has_function("parameters"):

            def getParameterInfo(self) -> Optional[list[arcpy.Parameter]]:
                return module.parameters()

        def isLicensed(self) -> bool:
            return True

        if module_has_function("updateParameters"):

            def updateParameters(self, parameters: list[arcpy.Parameter]) -> None:
                return module.update_parameters(parameters)

        if module_has_function("updateMessages"):

            def updateMessages(self, parameters: list[arcpy.Parameter]) -> None:
                return module.update_messages(parameters)

        if module_has_function("execute"):

            def execute(self, parameters: list[arcpy.Parameter], messages: Any) -> None:
                return module.execute(parameters)

        else:
            raise AttributeError(
                f"Module `{module}` has no function `execute`, but arcgis requires one exists in each tool."
            )

        if module_has_function("post_execute"):

            def postExecute(self, parameters: list[arcpy.Parameter]) -> None:
                return module.post_execute(parameters)

    return Tool


AppendToART = tool(
    "Append to ART",
    "Appends new integrated mains to the Asset Reference Table.",
    ToolCategory.MUTATION,
    False,
    append_to_art,
)

CalculateFacilityIdentifiers = tool(
    "Calculate Facility Identifiers",
    "Calculates FIDs and FID indices for specified water layers.",
    ToolCategory.MUTATION,
    False,
    calculate_fids,
)

WaterQualityControl = tool(
    "Water Quality Control",
    "Executes selected quality control checks on specified water layers.",
    ToolCategory.VALIDATION,
    False,
    quality_control,
)

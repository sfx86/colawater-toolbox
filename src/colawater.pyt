from enum import Enum, unique
from types import ModuleType
from typing import Any, Optional

import arcpy

from colawater.tools import append_art, fid_calculator, quality_control


class Toolbox:
    def __init__(self) -> None:
        self.label = "Columbia Water"
        self.alias = "colawater"
        self.tools = [
            AppendToART,
            CalculateFacilityIdentifiers,
            WaterQualityControl,
        ]


def tool(
    label: str,
    description: str,
    category: str,
    backgroundable: bool,
    module: ModuleType,
) -> type:
    def module_has_function(name: str) -> bool:
        return callable(getattr(module, name, None))

    class Tool:
        def __init__(self) -> None:
            self.label = label
            self.description = description
            self.category = category
            self.canRunInBackground = backgroundable

        def getParameterInfo(self) -> Optional[list[arcpy.Parameter]]:
            if module_has_function("parameters"):
                return module.parameters()

        def isLicensed(self) -> bool:
            return True

        def updateParameters(self, parameters: list[arcpy.Parameter]) -> None:
            if module_has_function("updateParameters"):
                module.update_parameters(parameters)

        def updateMessages(self, parameters: list[arcpy.Parameter]) -> None:
            if module_has_function("updateMessages"):
                module.update_messages(parameters)

        def execute(self, parameters: list[arcpy.Parameter], messages: Any) -> None:
            if module_has_function("execute"):
                module.execute(parameters)
            else:
                raise AttributeError(
                    f"Module `{module}` has no function `execute`, but arcgis requires one exists in each tool."
                )

        def postExecute(self, parameters: list[arcpy.Parameter]) -> None:
            if module_has_function("post_execute"):
                module.post_execute(parameters)

    return Tool


@unique
class _Category(Enum):
    VALIDATION = "Data Validation"
    MUTATION = "Update Layers"


AppendToART = tool(
    "Append to ART",
    "Appends new integrated mains to the Asset Reference Table.",
    _Category.MUTATION.value,
    False,
    append_art,
)

CalculateFacilityIdentifiers = tool(
    "Calculate Facility Identifiers",
    "Calculates FIDs and FID indices for specified water layers.",
    _Category.MUTATION.value,
    False,
    fid_calculator,
)

WaterQualityControl = tool(
    "Water Quality Control",
    "Executes selected quality control checks on specified water layers.",
    _Category.VALIDATION.value,
    False,
    quality_control,
)

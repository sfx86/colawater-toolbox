from colawater.lib.tool import toolshed
from colawater.toolbox import append_to_art, calculate_fids, quality_control


class Toolbox:
    def __init__(self) -> None:
        self.label = "Columbia Water"
        self.alias = "colawater"
        self.tools = [
            AppendToART,
            CalculateFacilityIdentifiers,
            WaterQualityControl,
        ]


AppendToART = toolshed(
    "Append to ART",
    "Appends new integrated mains to the Asset Reference Table.",
    parameters=append_to_art.parameters,
    execute=append_to_art.execute,
)

CalculateFacilityIdentifiers = toolshed(
    "Calculate Facility Identifiers",
    "Calculates FIDs and FID indices for specified water layers.",
    parameters=calculate_fids.parameters,
    execute=calculate_fids.execute,
)

WaterQualityControl = toolshed(
    "Water Quality Control",
    "Executes selected quality control checks on specified water layers.",
    parameters=quality_control.parameters,
    execute=quality_control.execute,
)

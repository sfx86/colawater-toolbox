from colawater.lib.tool import toolshed
from colawater.toolbox import (
    append_to_art,
    calculate_fids,
    dump_to_csv,
    quality_control,
)


class Toolbox:
    def __init__(self) -> None:
        self.label = "Columbia Water"
        self.alias = "colawater"
        self.tools = [
            AppendToART,
            CalculateFacilityIdentifiers,
            DumpToCSV,
            WaterQualityControl,
        ]


AppendToART = toolshed(
    "Append to ART",
    "Appends new integrated mains to the Asset Reference Table.",
    append_to_art.parameters,
    append_to_art.execute,
)

CalculateFacilityIdentifiers = toolshed(
    "Calculate Facility Identifiers",
    "Calculates FIDs and FID indices for specified water layers.",
    calculate_fids.parameters,
    calculate_fids.execute,
)

DumpToCSV = toolshed(
    "Dump to CSV",
    "Dumps full attribute tables of input layers to CSV files in the target directory.",
    dump_to_csv.parameters,
    dump_to_csv.execute,
)

WaterQualityControl = toolshed(
    "Water Quality Control",
    "Executes selected quality control checks on specified water layers.",
    quality_control.parameters,
    quality_control.execute,
)

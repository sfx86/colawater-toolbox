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
            append_to_art.AppendToART,
            calculate_fids.CalculateFacIDs,
            dump_to_csv.DumpToCSV,
            quality_control.QualityControl,
        ]

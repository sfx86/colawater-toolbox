from toolbox.append_to_art import AppendToART
from toolbox.calculate_fids import CalculateFacilityIdentifiers
from toolbox.quality_control import WaterQualityControl


class Toolbox:
    def __init__(self) -> None:
        self.label = "Columbia Water"
        self.alias = "colawater"
        self.tools = [
            AppendToART,
            CalculateFacilityIdentifiers,
            WaterQualityControl,
        ]

from colawater.toolbox import (
    AppendToART,
    CalculateFacIDs,
    QualityControl,
    UpdateAGOData,
)


class Toolbox:
    def __init__(self) -> None:
        self.label = "Columbia Water"
        self.alias = "colawater"
        self.tools = [
            # AppendToART,
            CalculateFacIDs,
            # QualityControl,
            UpdateAGOData,
        ]

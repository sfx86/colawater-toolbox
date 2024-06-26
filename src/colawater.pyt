from colawater.lib.mp import mp_fix_exec
from colawater.toolbox.calculate_fids.tool import CalculateFacilityIdentifiers
from colawater.toolbox.fetch_ago_data.tool import FetchAGOData

mp_fix_exec()


class Toolbox:
    def __init__(self) -> None:
        self.label = "Columbia Water"
        self.alias = "colawater"
        self.tools = [
            CalculateFacilityIdentifiers,
            FetchAGOData,
        ]

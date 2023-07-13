import arcpy
import tools
from importlib import reload

reload(tools)

class Toolbox(object):
    def __init__(self):
        self.label = "Columbia Water"
        self.alias = "ColaWater"
        self.tools = [CalculateFacilityIdentifiers]


class CalculateFacilityIdentifiers(object):
    def __init__(self) -> None:
        self.label = "Calculate Facility Identifiers"
        self.description = "Calculates the various facility identifiers and facility identifier indices for water layers."
        self.canRunInBackground = False

    def getParameterInfo(self) -> list[arcpy.Parameter]:
        return tools.fids.parameters()

    def isLicensed(self) -> bool:
        return True

    def updateParameters(self, parameters: list[arcpy.Parameter]) -> None:
        tools.fids.update_parameters(parameters)

    def updateMessages(self, parameters: list[arcpy.Parameter]) -> None:
        tools.fids.update_messages(parameters)

    def execute(self, parameters: list[arcpy.Parameter], messages) -> None:
        tools.fids.execute(parameters)

    def postExecute(self, parameters: list[arcpy.Parameter]) -> None:
        tools.fids.post_execute(parameters)

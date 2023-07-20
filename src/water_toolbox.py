import arcpy
from colawater import tools


class Toolbox(object):
    def __init__(self) -> None:
        self.label = "Columbia Water"
        self.alias = "ColaWater"
        self.tools = [CalculateFacilityIdentifiers, QualityControl]


class CalculateFacilityIdentifiers(object):
    def __init__(self) -> None:
        self.label = "Calculate Facility Identifiers"
        self.description = "Calculates FIDs and FID indices for specified water layers."
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


class QualityControl(object):
    def __init__(self) -> None:
        self.label = "Water Quality Control"
        self.description = (
            "Executes selected quality control checks on specified water layers."
        )
        self.canRunInBackground = False

    def getParameterInfo(self) -> list[arcpy.Parameter]:
        return tools.qc.parameters()

    def isLicensed(self) -> bool:
        return True

    def updateParameters(self, parameters: list[arcpy.Parameter]) -> None:
        tools.qc.update_parameters(parameters)

    def updateMessages(self, parameters: list[arcpy.Parameter]) -> None:
        tools.qc.update_messages(parameters)

    def execute(self, parameters: list[arcpy.Parameter], messages) -> None:
        tools.qc.execute(parameters)

    def postExecute(self, parameters: list[arcpy.Parameter]) -> None:
        tools.qc.post_execute(parameters)

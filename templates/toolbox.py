from typing import Any

import arcpy

from colawater.tools import toolname


class Tool:
    def __init__(self) -> None:
        self.label = ""
        self.description = ""
        self.canRunInBackground = False

    def getParameterInfo(self) -> list[arcpy.Parameter]:
        return toolname.parameters()

    def isLicensed(self) -> bool:
        return True

    def updateParameters(self, parameters: list[arcpy.Parameter]) -> None:
        toolname.update_parameters(parameters)

    def updateMessages(self, parameters: list[arcpy.Parameter]) -> None:
        toolname.update_messages(parameters)

    def execute(self, parameters: list[arcpy.Parameter], messages: Any) -> None:
        toolname.execute(parameters)

    def postExecute(self, parameters: list[arcpy.Parameter]) -> None:
        toolname.post_execute(parameters)

from typing import Any

import arcpy


class Tool:
    category = ""
    label = ""
    description = ""
    canRunInBackground = False

    def execute(self, parameters: list[arcpy.Parameter], messages) -> None:
        return None

    def getParameterInfo(self) -> list[arcpy.Parameter]:
        return []

    # fmt: off
    def isLicensed(self) -> bool: return True
    def postExecute(self, parameters: list[arcpy.Parameter]) -> None: return None
    def updateMessages(self, parameters: list[Any]) -> None: return None
    def updateParameters(self, parameters: list[arcpy.Parameter]) -> None: return None
    # fmt: on

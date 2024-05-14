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

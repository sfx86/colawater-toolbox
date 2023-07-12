import arcpy
import template

class Template(object):
    def __init__(self):
        self.label = ""
        self.description = ""
        self.canRunInBackground = False

    def getParameterInfo(self) -> list[arcpy.Parameter]:
        return template.parameters()

    def isLicensed(self) -> bool:
        return True

    def updateParameters(self, parameters: list[arcpy.Parameter]) -> None:
        template.update_parameters(parameters)

    def updateMessages(self, parameters: list[arcpy.Parameter]) -> None:
        template.update_messages(parameters)

    def execute(self, parameters: list[arcpy.Parameter], messages) -> None:
        template.execute(parameters)

    def postExecute(self, parameters: list[arcpy.Parameter]) -> None:
        template.post_execute(parameters)
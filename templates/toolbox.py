import arcpy

from colawater import tools


class Tool:
    """
    Contains metadata and methods for the {} tool.

    Attributes:
        label (str): The tool label.
        description (str): The tool description.
        canRunInBackground (bool): Whether the tool can run in the background.

    Note:
        Implementation details and method descriptions can be found in the
        documentation for ``colawater.tools.{}``.
    """

    def __init__(self) -> None:
        self.label = ""
        self.description = ""
        self.canRunInBackground = False

    def getParameterInfo(self) -> list[arcpy.Parameter]:
        return tools.tool.parameters()

    def isLicensed(self) -> bool:
        return True

    def updateParameters(self, parameters: list[arcpy.Parameter]) -> None:
        tools.tool.update_parameters(parameters)

    def updateMessages(self, parameters: list[arcpy.Parameter]) -> None:
        tools.tool.update_messages(parameters)

    def execute(self, parameters: list[arcpy.Parameter], messages: Any) -> None:
        tools.tool.execute(parameters)

    def postExecute(self, parameters: list[arcpy.Parameter]) -> None:
        tools.quality_control.post_execute(parameters)

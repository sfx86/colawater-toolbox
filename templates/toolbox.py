import arcpy
from colawater import tools


class Tool:
    """
    Contains metadata and methods for the {} tool.

    Attributes:
        label (str): The tool label.
        description (str): The tool description.
        canRunInBackground (bool): Whether the tool can run in the background.
    """

    def __init__(self) -> None:
        self.label = ""
        self.description = ""
        self.canRunInBackground = False

    def getParameterInfo(self) -> list[arcpy.Parameter]:
        """
        Returns paramater definitions for this tool.

        Returns:
            list[arpcy.Parameter]: A list of parameter definitions.
        """
        return tools.tool.parameters()

    def isLicensed(self) -> bool:
        """
        Returns whether this tool is licensed to run.

        Returns:
            bool: Whether this tool is license to run.
        """
        return True

    def updateParameters(self, parameters: list[arcpy.Parameter]) -> None:
        """
        Modifies the parameters to ensure they work with this tool.

        Note:
            Runs every time a parameter is changed.
        """
        tools.tool.update_parameters(parameters)

    def updateMessages(self, parameters: list[arcpy.Parameter]) -> None:
        """
        Modifies the messages created by internal validation.

        Note:
            Runs after internal validation.
        """
        tools.tool.update_messages(parameters)

    def execute(self, parameters: list[arcpy.Parameter], messages: Any) -> None:
        """
        Entry point for the tool.
        """
        tools.tool.execute(parameters)

    def postExecute(self, parameters: list[arcpy.Parameter]) -> None:
        """
        Runs after ``execute()``
        """
        tools.quality_control.post_execute(parameters)

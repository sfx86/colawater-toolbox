import arcpy
from colawater import tools
from typing import Any


class Toolbox:
    """
    Contains metadata about the toolbox and what tools it holds.

    ArcGIS ingests this class and uses it to create the geoprocessing tools' UIs
    and use their functionality by calling known methods on the classes included in
    ``self.tools``.
    Said methods can be found in the `Python toolbox template <template_>`_.


    Attributes:
        label (str): The toolbox label.
        alias (str): The toolbox alias.
        tools (list[Any]): A list of the tools associated with this toolbox.

    .. _template: https://pro.arcgis.com/en/pro-app/latest/arcpy/geoprocessing_and_python/a-template-for-python-toolboxes.htm
    """

    def __init__(self) -> None:
        """
        Initialize toolbox metadata.
        """
        self.label = "Columbia Water"
        self.alias = "ColaWater"
        self.tools = [CalculateFacilityIdentifiers, WaterQualityControl]


class CalculateFacilityIdentifiers:
    """
    Contains metadata and methods for the Calculate Facility Identifiers tool.

    Attributes:
        label (str): The tool label.
        description (str): The tool description.
        canRunInBackground (bool): Whether the tool can run in the background.
    """

    def __init__(self) -> None:
        self.label = "Calculate Facility Identifiers"
        self.description = "Calculates FIDs and FID indices for specified water layers."
        self.canRunInBackground = False

    def getParameterInfo(self) -> list[arcpy.Parameter]:
        """
        Returns paramater definitions for this tool.

        Returns:
            list[arpcy.Parameter]: A list of parameter definitions.
        """
        return tools.fid_calculator.parameters()

    def isLicensed(self) -> bool:
        """
        Returns whether this tool is licensed to run.

        Returns:
            bool: Whether this tool is licensed to run.
        """
        return True

    def updateParameters(self, parameters: list[arcpy.Parameter]) -> None:
        """
        Modifies the parameters to ensure they work with this tool.

        Note:
            Runs every time a parameter is changed.
        """
        tools.fid_calculator.update_parameters(parameters)

    def updateMessages(self, parameters: list[arcpy.Parameter]) -> None:
        """
        Modifies the messages created by internal validation.

        Note:
            Runs after internal validation.
        """
        tools.fid_calculator.update_messages(parameters)

    def execute(self, parameters: list[arcpy.Parameter], messages: Any) -> None:
        """
        Entry point for the tool.
        """
        tools.fid_calculator.execute(parameters)

    def postExecute(self, parameters: list[arcpy.Parameter]) -> None:
        """
        Runs after ``execute()``
        """
        tools.fid_calculator.post_execute(parameters)


class WaterQualityControl:
    """
    Contains metadata and methods for the Water Quality Control tool.

    Attributes:
        label (str): The tool label.
        description (str): The tool description.
        canRunInBackground (bool): Whether the tool can run in the background.
    """

    def __init__(self) -> None:
        self.label = "Water Quality Control"
        self.description = (
            "Executes selected quality control checks on specified water layers."
        )
        self.canRunInBackground = False

    def getParameterInfo(self) -> list[arcpy.Parameter]:
        """
        Returns paramater definitions for this tool.

        Returns:
            list[arpcy.Parameter]: A list of parameter definitions.
        """
        return tools.quality_control.parameters()

    def isLicensed(self) -> bool:
        """
        Returns whether this tool is licensed to run.

        Returns:
            bool: Whether this tool is licensed to run.
        """
        return True

    def updateParameters(self, parameters: list[arcpy.Parameter]) -> None:
        """
        Modifies the parameters to ensure they work with this tool.

        Note:
            Runs every time a parameter is changed.
        """
        tools.quality_control.update_parameters(parameters)

    def updateMessages(self, parameters: list[arcpy.Parameter]) -> None:
        """
        Modifies the messages created by internal validation.

        Note:
            Runs after internal validation.
        """
        tools.quality_control.update_messages(parameters)

    def execute(self, parameters: list[arcpy.Parameter], messages: Any) -> None:
        """
        Entry point for the tool.
        """
        tools.quality_control.execute(parameters)

    def postExecute(self, parameters: list[arcpy.Parameter]) -> None:
        """
        Runs after ``execute()``
        """
        tools.quality_control.post_execute(parameters)

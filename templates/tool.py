import arcpy

from colawater.utils.constants import *
from colawater.utils.functions import *
from colawater.utils.status import StatusUpdater
from colawater.utils.summary import SummaryBuilder, SummaryCollection


def execute(parameters: list[arcpy.Parameter]) -> None:
    """
    Entry point for {}.

    Description.

    Raises:
        ExecutionError: An error ocurred in the tool execution.
    """
    arcpy.SetProgressor("step", "", 0, 99)
    status = StatusUpdater()
    summary = SummaryBuilder()

    #

    summary.post()


def post_execute(parameters: list[arcpy.Parameter]) -> None:
    """
    Note:
        Unimplemented for this tool.
    """
    pass


def parameters() -> list[arcpy.Parameter]:
    """
    Return the parameters for {}.

    Returns:
        list[arcpy.Parameter]: The list of parameters.
    """
    template = arcpy.Parameter(
        displayName="",
        name="",
        datatype="",
        parameterType="Required",
        direction="Input",
    )

    return [template]


def update_parameters(parameters: list[arcpy.Parameter]) -> None:
    """
    Update parameters to ensure their correctness.

    Arguments:
        parameters (list[arcpy.Parameter]): The list of parameters.
    """
    pass


def update_messages(parameters: list[arcpy.Parameter]) -> None:
    """
    Note:
        Unimplemented for this tool.
    """
    pass

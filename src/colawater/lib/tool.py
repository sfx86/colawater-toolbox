"""
Type factory for building arcpy tools.

Examples:
    .. code-block:: python
    
        Foo = toolshed(
            "Foo",
            "Performs arbitrary incantations on your database.",
            some_module.parameters,
            some_module.execute,
        )

"""
from typing import Any, Callable, Optional

import arcpy


def toolshed(
    label: str,
    description: str,
    parameters: Callable[[], list[arcpy.Parameter]],
    execute: Callable[[list[arcpy.Parameter]], None],
    category: Optional[str] = None,
    backgroundable: bool = False,
    update_parameters: Callable[[list[arcpy.Parameter]], None] = lambda _: None,
    update_messages: Callable[[list[arcpy.Parameter]], None] = lambda _: None,
    post_execute: Callable[[list[arcpy.Parameter]], None] = lambda _: None,
) -> type:
    """
    Returns a tool class in the shape expected by ArcPy.

    Arguments:
        label (str):
        description (str):
        parameters (Callable[[], list[arcpy.Parameter]]): A function providing the tool parameters.
        execute (Callable[[list[arcpy.Parameter]], None]): The tool's entry point.
        category (Optional[str]):
            A tool category. Defaults to None.
        backgroundable (bool):
            Whether the tool can be backgrounded. Defaults to False.
        update_parameters (Callable[[list[arcpy.Parameter]], None]):
            A function that updates the parameter values.
            Defaults to ``lambda _: None``.
        update_messages (Callable[[list[arcpy.Parameter]], None]):
            A function that updates parameter messages.
            Defaults to ``lambda _: None``.
        post_execute (Callable[[list[arcpy.Parameter]], None]):
            A function to be run after execute runs.
            Defaults to ``lambda _: None``.

    Returns:
        type: A class with all the required attributes and methods for use in a toolbox.
    """

    class Tool:
        def __init__(self) -> None:
            self.label = label
            self.description = description
            self.category = category
            self.canRunInBackground = backgroundable

        def getParameterInfo(self) -> list[arcpy.Parameter]:
            return parameters()

        def isLicensed(self) -> bool:
            return True

        def updateParameters(self, parameters: list[arcpy.Parameter]) -> None:
            return update_parameters(parameters)

        def updateMessages(self, parameters: list[arcpy.Parameter]) -> None:
            return update_messages(parameters)

        def execute(self, parameters: list[arcpy.Parameter], messages: Any) -> None:
            return execute(parameters)

        def postExecute(self, parameters: list[arcpy.Parameter]) -> None:
            return post_execute(parameters)

    return Tool

from typing import Any, Callable, Optional

import arcpy


def toolshed(
    label: str,
    description: str,
    category: Optional[str] = None,
    backgroundable: bool = False,
    parameters: Callable[[], list[arcpy.Parameter]] = lambda: [],
    update_parameters: Callable[[list[arcpy.Parameter]], None] = lambda _: None,
    update_messages: Callable[[list[arcpy.Parameter]], None] = lambda _: None,
    execute: Callable[[list[arcpy.Parameter]], None] = lambda _: None,
    post_execute: Callable[[list[arcpy.Parameter]], None] = lambda _: None,
) -> type:
    class Tool:
        def __init__(
            self,
        ) -> None:
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

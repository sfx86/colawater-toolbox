from typing import Any, Callable, Optional

import arcpy


class Tool:
    def __init__(
        self,
        label: str,
        description: str,
        category: Optional[str] = None,
        backgroundable: bool = False,
        parameters: Callable[[], list[arcpy.Parameter]] = lambda: [],
        update_parameters: Callable[[list[arcpy.Parameter]], None] = lambda _: None,
        update_messages: Callable[[list[arcpy.Parameter]], None] = lambda _: None,
        execute: Callable[[list[arcpy.Parameter]], None] = lambda _: None,
        post_execute: Callable[[list[arcpy.Parameter]], None] = lambda _: None,
    ) -> None:
        self.label = label
        self.description = description
        self.category = category
        self.canRunInBackground = backgroundable

        self._parameters = parameters
        self._update_parameters = update_parameters
        self._update_messages = update_messages
        self._execute = execute
        self._post_execute = post_execute

    def getParameterInfo(self) -> list[arcpy.Parameter]:
        return self._parameters()

    def isLicensed(self) -> bool:
        return True

    def updateParameters(self, parameters: list[arcpy.Parameter]) -> None:
        return self._update_parameters(parameters)

    def updateMessages(self, parameters: list[arcpy.Parameter]) -> None:
        return self._update_messages(parameters)

    def execute(self, parameters: list[arcpy.Parameter], messages: Any) -> None:
        return self._execute(parameters)

    def postExecute(self, parameters: list[arcpy.Parameter]) -> None:
        return self._post_execute(parameters)

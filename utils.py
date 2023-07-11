import arcpy


def getLayerPath(layer) -> str:
    """Return an absolute path to a layer."""
    # https://pro.arcgis.com/en/pro-app/latest/arcpy/functions/describe.htm
    desc = arcpy.Describe(layer)
    # create absolute path to layer using described layer info
    return f"{desc.path}\\{desc.name}"


class StatusUpdater:
    """A wrapper class for updating the arcpy progressor and arcpy messages at once."""

    def __init__(self, messages: list) -> None:
        self.messages = messages

    def update_warn(self, content: str) -> None:
        """Add a warning message, set the progressor label, and update the progressor position."""
        self.messages.addWarningMessage(content)
        arcpy.SetProgressorLabel(content)
        arcpy.SetProgressorPosition()

    def update_info(self, content: str) -> None:
        """Add a message, set the progressor label, and update the progressor position."""
        self.messages.addMessage(content)
        arcpy.SetProgressorLabel(content)
        arcpy.SetProgressorPosition()

    def update_err(self, content: str) -> None:
        """Add an error message and raise an ExecutionErorr."""
        self.messages.addErrorMessage(content)
        raise arcpy.ExecuteError(content)

    def bump_progressor(self, position=1):
        """Increment progressor by a given value."""
        arcpy.SetProgressorPosition(position)


class SummaryBuilder:
    """A helper class for iteratively building tool execution summaries."""

    def __init__(self, messages):
        self.messages = messages
        self._content = ""

    def add_header(self, content: str) -> None:
        """Add a header to the summary's content."""
        if self._content:
            self._content += f"\n{content}\n"
        else:
            self._content += f"{content}\n"

    def add_item(self, content: str) -> None:
        """Add an item to the summary's content."""
        self._content += f"\t{content}\n"

    def clear(self) -> None:
        """Clear the summary's content."""
        self._content = ""

    def post(self) -> None:
        """Add a message with the summary's content."""
        self.messages.addMessage(self._content)

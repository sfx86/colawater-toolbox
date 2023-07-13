import arcpy


class StatusUpdater:
    """A wrapper class for updating the arcpy progressor and arcpy messages at once."""

    def __init__(self) -> None:
        pass

    def update_warn(self, content: str) -> None:
        """Add a warning message, set the progressor label, and update the progressor position."""
        arcpy.AddWarning(content)
        arcpy.SetProgressorLabel(content)
        arcpy.SetProgressorPosition()

    def update_info(self, content: str) -> None:
        """Add a message, set the progressor label, and update the progressor position."""
        arcpy.AddMessage(content)
        arcpy.SetProgressorLabel(content)
        arcpy.SetProgressorPosition()

    def update_err(self, content: str) -> None:
        """Add an error message and raise an ExecutionErorr."""
        arcpy.AddError(content)
        raise arcpy.ExecuteError(content)

    def bump_progressor(self, position=1):
        """Increment progressor by a given value."""
        arcpy.SetProgressorPosition(position)

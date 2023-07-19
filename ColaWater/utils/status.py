import arcpy


class StatusUpdater:
    """A wrapper class for updating the arcpy progressor and arcpy messages at once."""

    def __init__(self) -> None:
        pass

    def update_warn(self, content: str, bump=True) -> None:
        """Add a warning message and update the progressor label and position."""
        arcpy.AddWarning(content)
        self.update_label(content)
        if bump:
            self.bump_progressor()

    def update_info(self, content: str, bump=True) -> None:
        """Add a message and update the progressor label and position."""
        arcpy.AddMessage(content)
        self.update_label(content)
        if bump:
            self.bump_progressor()

    def update_err(self, content: str) -> None:
        """Add an error message and raise an ExecutionError."""
        arcpy.AddError(content)
        raise arcpy.ExecuteError(content)

    def update_label(self, content: str) -> None:
        arcpy.SetProgressorLabel(content)

    def bump_progressor(self, position=1) -> None:
        """Increment progressor by a given value."""
        arcpy.SetProgressorPosition(position)

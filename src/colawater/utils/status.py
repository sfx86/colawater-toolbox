"""
Contains 

Examples:
    .. code-block:: python

        status = StatusUpdater()

        status.update_label("Example usage")
        status.increment_progressor(2)
        status.update_info("info")
        status.update_warn("warning", increment=False)

        if something_happens():
            status.update_err("error") # Raises ExecutionError
"""

import arcpy


class StatusUpdater:
    """
    A wrapper class for updating the arcpy progressor and arcpy messages simultaneously.
    """

    def __init__(self) -> None:
        pass

    def update_warn(self, content: str, increment: bool = True) -> None:
        """
        Adds a warning message and update the progressor label and position.

        Arguments:
            content (str): The message content to be added.
            bump (bool): Whether to increment the progressor.
        """
        arcpy.AddWarning(content)
        self.update_label(content)
        if increment:
            self.increment_progressor()

    def update_info(self, content: str, increment: bool = True) -> None:
        """
        Adds a message and update the progressor label and position.

        Arguments:
            content (str): The message content to be added.
            bump (bool): Whether to increment the progressor.
        """
        arcpy.AddMessage(content)
        self.update_label(content)
        if increment:
            self.increment_progressor()

    def update_err(self, content: str) -> None:
        """
        Adds an error message and raise an ExecutionError.

        Arguments:
            content (str): The message content to be added.

        Raises:
            ExecutionError: This method will always raise this exception.
        """
        arcpy.AddError(content)
        raise arcpy.ExecuteError(content)

    def update_label(self, content: str) -> None:
        """
        Updates the progressor label.

        Arguments:
            content (str): The message content to be added.
        """
        arcpy.SetProgressorLabel(content)

    def increment_progressor(self, position: int = 1) -> None:
        """
        Increments progressor by a given value.

        Arguments:
            position (int): The amount to increment the progressor.
        """
        arcpy.SetProgressorPosition(position)

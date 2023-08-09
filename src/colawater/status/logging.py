"""
A wrapper for the arcpy messages and progressor APIs.

The functions provided here correspond to the arcpy warning levels:
``info()`` adds a message of severity 0, ``warning()`` of severity 1, and
``error()`` of severity 2.
All of these functions also update the progressor label.

Examples:
    .. code-block:: python

        import colawater.status.logging as log

        log.info("helpful message")
        log.warning("warning message")
        log.error("error message")
"""

import arcpy

from colawater.status import progressor


def info(content: str) -> None:
    """
    Adds a message and updates the progressor label.

    Arguments:
        content (str): The message content to be added.
    """
    arcpy.AddMessage(content)
    progressor.label(content)


def warning(content: str) -> None:
    """
    Adds a warning message and updates the progressor label.

    Arguments:
        content (str): The message content to be added.
    """
    arcpy.AddWarning(content)
    progressor.label(content)


def error(content: str) -> None:
    """
    Adds an error message.

    Arguments:
        content (str): The message content to be added.
    """
    arcpy.AddError(content)
    progressor.label(content)

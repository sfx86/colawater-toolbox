"""
A wrapper for some arcpy progressor methods.

Examples:
    .. code-block: python

        import colawater.status.progressor as pg

        pg.label("helpful message")
        pg.increment(10) # Defaults to 1
"""
from enum import Enum, auto
from typing import Any

import arcpy


class _ProgressorType(Enum):
    DEFAULT = auto()
    STEP = auto()


_progressor_type = _ProgressorType.DEFAULT


def set_progressor(*args: Any, **kwargs: Any) -> None:
    """
    Transparently wraps ``arcpy.SetProgressor()``, but also tracks the type of the
    progressor to ensure safe usage.

    Arguments:
        *args (Any): The positional arguments to ``arcpy.SetProgressor()``
        **kwargs (Any): The keyword arguments to ``arcpy.SetProgressor()``
    """
    global _progressor_type

    local_prog_type = str(args[0]).lower()

    if local_prog_type == "step":
        _progressor_type = _ProgressorType.STEP
    else:
        _progressor_type = _ProgressorType.DEFAULT

    arcpy.SetProgressor(*args, **kwargs)


def label(content: str) -> None:
    """
    Updates the progressor label.

    Arguments:
        content (str): The message content to be added.
    """
    arcpy.SetProgressorLabel(content)


def increment(position: int = 1) -> None:
    """
    Increments the progressor by a given value.

    Raises an exception if used with a DEFAULT progressor.

    Arguments:
        position (int): The amount to increment the progressor.

    Raises:
        TypeError: this function was called with an active progressor of type DEFAULT.
    """
    if _progressor_type == _ProgressorType.DEFAULT:
        raise TypeError("Cannot call `increment` on a progressor of type DEFAULT.")
    arcpy.SetProgressorPosition(position)

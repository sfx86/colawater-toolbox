"""
A wrapper for some arcpy progressor methods.

Examples:
    .. code-block:: python

        import colawater.status.progressor as pg

        pg.set_progressor("step")
        pg.label("helpful message")
        pg.increment() # Defaults to 1, will raise TypeError if used on a default progressor
"""
from enum import Enum, auto, unique
from typing import Any

import arcpy


@unique
class _ProgressorType(Enum):
    DEFAULT = auto()
    STEP = auto()


_progressor_type = _ProgressorType.DEFAULT


def set_progressor(*args: Any, **kwargs: Any) -> None:
    """
    Transparently wraps ``arcpy.SetProgressor()``, but also tracks the progressor type to ensure safe usage.

    Arguments:
        *args (Any): The positional arguments to ``arcpy.SetProgressor()``
        **kwargs (Any): The keyword arguments to ``arcpy.SetProgressor()``
    """
    arcpy.SetProgressor(*args, **kwargs)

    global _progressor_type

    local_prog_type = str(args[0]).lower()

    if local_prog_type == "step":
        _progressor_type = _ProgressorType.STEP
    else:
        _progressor_type = _ProgressorType.DEFAULT


def label(content: str) -> None:
    """
    Updates the progressor label.

    Arguments:
        content (str): A string containing the text to display as the progressor label.
    """
    arcpy.SetProgressorLabel(content)


def increment(position: int = 1) -> None:
    """
    Increments the progressor by a given value.

    Arguments:
        position (int): The amount to increment the progressor.

    Raises:
        TypeError: The active progressor is not of type STEP.
    """
    if _progressor_type == _ProgressorType.DEFAULT:
        raise TypeError("Can only call `increment` on a progressor of type STEP.")
    arcpy.SetProgressorPosition(position)

"""
A wrapper for some arcpy progressor methods.

Currently, this module wraps the functions with no added functionality, 
but some could come in the future. 

Examples:
    .. code-block: python
        import colawater.status.progressor as pg

        pg.label("helpful message")
        pg.increment(10) # Defaults to 1
"""
import arcpy


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

    Arguments:
        position (int): The amount to increment the progressor.
    """
    arcpy.SetProgressorPosition(position)

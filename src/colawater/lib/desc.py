"""
Wrapper functions around ``arcpy.Describe`` that improve the interface for paths.

Examples:
    .. code-block:: python

        full_path = path(item) # Returns "path/to/item".
        basename = basename(item) # Returns "item".
        path = path(item) # Returns "path/to".
"""

from typing import Any

import arcpy


def full_path(item: Any) -> str:
    """
    Returns the full path to a item.

    Arguments:
        item (arcpy._mp.Layer): A item object.

    Returns:
        str: The absolute path to the item.
    """
    desc = arcpy.Describe(item)
    path: str = "\\".join(
        (
            desc.path,  # pyright: ignore [reportAttributeAccessIssue]
            desc.name,  # pyright: ignore [reportAttributeAccessIssue]
        )
    )

    return path


def basename(item: Any) -> str:
    """
    Returns the item's base name.

    Arguments:
        item (arcpy._mp.Layer): A item object.

    Returns:
        str: The item's base name.
    """
    basename: str = arcpy.Describe(
        item
    ).name  # pyright: ignore [reportAttributeAccessIssue]

    return basename


def path(item: Any) -> str:
    """
    Returns the path to a item excluding the base name.

    Arguments:
        item (arcpy._mp.Layer): A item object.

    Returns:
        str: The path to a item excluding the base name.
    """
    path: str = arcpy.Describe(
        item
    ).path  # pyright: ignore [reportAttributeAccessIssue]

    return path

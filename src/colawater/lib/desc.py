"""
Wrapper functions around ``arcpy.Describe`` that improve the interface.

Examples:
    .. code-block:: python

        path = path(item) # Returns "path/to/item".
        basename = basename(item) # Returns "item".
        workspace = workspace(item) # Returns "path/to/workspace.
                                     # This is the same as the value in ``path``,
                                     # but without the item name.
        has_objectid = has_field(item, "OBJECTID") # Returns True.
"""

from typing import Any

import arcpy


def path(item: Any) -> str:
    """
    Returns the full path to a item.

    Arguments:
        item (arcpy._mp.Layer): A item object.

    Returns:
        str: The absolute path to the item.
    """
    desc = arcpy.Describe(item)
    path = "\\".join(
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
    name = arcpy.Describe(item).name  # pyright: ignore [reportAttributeAccessIssue]
    # foo\bar\baz -> baz
    basename = name.rpartition("\\")[2]

    return basename


def workspace(item: Any) -> str:
    """
    Returns the path to a item's workspace.

    Arguments:
        item (arcpy._mp.Layer): A item object.

    Returns:
        str: The absolute path to the item's workspace.
    """
    path = arcpy.Describe(item).path  # pyright: ignore [reportAttributeAccessIssue]
    # foo\bar -> foo
    workspace = path.rpartition("\\")[0]

    return workspace

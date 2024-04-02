"""
Functions for working with layers.

Examples:
    .. code-block:: python

        path = path(layer) # Returns "path/to/layer".
        basename = basename(layer) # Returns "layer".
        workspace = workspace(layer) # Returns "path/to/workspace.
                                     # This is the same as the value in ``path``,
                                     # but without the layer name.
        has_objectid = has_field(layer, "OBJECTID") # Returns True.
"""

import arcpy


def path(
    layer: arcpy._mp.Layer,  # pyright: ignore [reportAttributeAccessIssue]
) -> str:
    """
    Returns the full path to a layer.

    Arguments:
        layer (arcpy._mp.Layer): A layer object.

    Returns:
        str: The absolute path to the layer.
    """
    desc = arcpy.Describe(layer)
    path = "\\".join(
        (
            desc.path,  # pyright: ignore [reportAttributeAccessIssue]
            desc.name,  # pyright: ignore [reportAttributeAccessIssue]
        )
    )

    return path


def basename(
    layer: arcpy._mp.Layer,  # pyright: ignore [reportAttributeAccessIssue]
) -> str:
    """
    Returns the layer's base name.

    Arguments:
        layer (arcpy._mp.Layer): A layer object.

    Returns:
        str: The layer's base name.
    """
    name = arcpy.Describe(layer).name  # pyright: ignore [reportAttributeAccessIssue]
    # foo\bar\baz -> baz
    basename = name.rpartition("\\")[2]

    return basename


def workspace(
    layer: arcpy._mp.Layer,  # pyright: ignore [reportAttributeAccessIssue]
) -> str:
    """
    Returns the path to a layer's workspace.

    Arguments:
        layer (arcpy._mp.Layer): A layer object.

    Returns:
        str: The absolute path to the layer's workspace.
    """
    path = arcpy.Describe(layer).path  # pyright: ignore [reportAttributeAccessIssue]
    # foo\bar -> foo
    workspace = path.rpartition("\\")[0]

    return workspace


def has_field(
    layer: arcpy._mp.Layer,  # pyright: ignore [reportAttributeAccessIssue]
    field_name: str,
) -> bool:
    """
    Returns whether a layer contains a field.

    This function wraps arcpy.ListFields, so if ``field_name`` contains ``*``, it will behave as a wildcard.
    E.g. ``Water*`` matches ``Water`` and ``Waterloo``.
    This function returns true if 1 or more matches are found, false if less.

    Arguments:
        layer (arcpy._mp.Layer): A layer object.
        field_name (str): The name of a field.

    Returns:
        bool: Whether ``layer`` contains ``field_name``
    """
    return bool(arcpy.ListFields(layer, field_name))

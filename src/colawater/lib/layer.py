"""
Wrapper functions for working with layers.

Examples:

    .. code-block:: python

        has_objectid = has_field(layer, "OBJECTID")
"""

import arcpy


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

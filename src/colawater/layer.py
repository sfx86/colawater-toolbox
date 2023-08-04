"""
Utilities for working with layers.

Examples:
    .. code-block:: python

        layer = layer_from_somewhere()
        path = get_layer_path(layer) # Returns "path/to/layer".
        workspace = get_workspace_path(layer) # Returns "path/to/workspace.
                                              # This is the same as the value in ``path``,
                                              # but without the layer name.
                                              
    Note: 
        Layer names include the groups of which they are a part.
        E.g., layer "foo" in group "bar" has a layer name of "bar\\foo"
"""
import arcpy


def get_path(layer: arcpy._mp.Layer) -> str:  # type: ignore
    """
    Returns the absolute path to a layer.

    Uses ``arcpy.Describe(layer)`` to get layer information and build a path.

    Arguments:
        layer (arcpy._mp.Layer): A layer object.

    Returns:
        str: The absolute path to the layer.
    """
    desc = arcpy.Describe(layer)
    return f"{desc.path}\\{desc.name}"  # type: ignore


def get_workspace(layer: arcpy._mp.Layer) -> str:  # type: ignore
    """
    Returns the absolute path to a layer's workspace.

    Uses ``arcpy.Describe(layer)`` to get layer information and build a path.

    Arguments:
        layer (arcpy._mp.Layer): A layer object.

    Returns:
        str: The absolute path to the layer's workspace.
    """
    return str(arcpy.Describe(layer).path)  # type: ignore

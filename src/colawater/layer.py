"""
Utilities for working with layers.

Examples:
    .. code-block:: python

        import colawater.layer as ly

        layer = layer_from_somewhere()
        path = ly.get_path(layer) # Returns "path/to/layer".
        workspace = ly.get_workspace(layer) # Returns "path/to/workspace.
                                            # This is the same as the value in ``path``,
                                            # but without the layer name.
                                              
    Note: 
        Layer names include the groups of which they are a part.
        Nested groups appear in parent-child order.
        E.g., layer "foo" in subgroup "bar" in group "baz" has a 
        layer name of "baz\\bar\\foo"
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

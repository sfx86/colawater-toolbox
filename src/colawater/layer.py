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


def get_path(
    layer: arcpy._mp.Layer,  # pyright: ignore [reportGeneralTypeIssues]
) -> str:
    """
    Returns the absolute path to a layer.

    Arguments:
        layer (arcpy._mp.Layer): A layer object.

    Returns:
        str: The absolute path to the layer.
    """
    desc = arcpy.Describe(layer)
    return f"{desc.path}\\{desc.name}"  # pyright: ignore [reportGeneralTypeIssues]


def get_workspace(
    layer: arcpy._mp.Layer,  # pyright: ignore [reportGeneralTypeIssues]
) -> str:
    """
    Returns the absolute path to a layer's workspace.

    Arguments:
        layer (arcpy._mp.Layer): A layer object.

    Returns:
        str: The absolute path to the layer's workspace.
    """
    path: str = arcpy.Describe(layer).path  # pyright: ignore [reportGeneralTypeIssues]
    slash_idx = path.rfind("\\")
    return path[:slash_idx]

"""
Utilities for working with layers.

Examples:
    .. code-block:: python

        import colawater.layer as ly

        layer = layer_from_somewhere()
        path = ly.path(layer) # Returns "path/to/layer".
        workspace = ly.workspace(layer) # Returns "path/to/workspace.
                                        # This is the same as the value in ``path``,
                                        # but without the layer name.
                                              
    Note: 
        Layer names include the groups of which they are a part.
        Nested groups appear in parent-child order.
        E.g., layer "foo" in subgroup "bar" in group "baz" has a 
        layer name of "baz\\bar\\foo"
"""
import re
from dataclasses import dataclass
from enum import Enum, unique
from typing import Optional

import arcpy


def name(
    layer: arcpy._mp.Layer,  # pyright: ignore [reportGeneralTypeIssues]
) -> str:
    """
    Returns the layer's base name.

    Arguments:
        layer (arcpy._mp.Layer): A layer object.

    Returns:
        str: The layer's name.
    """
    name: str = arcpy.Describe(layer).name  # pyright: ignore [reportGeneralTypeIssues]
    slash_idx = name.rfind("\\")
    return name[slash_idx + 1 :]


def path(
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


def workspace(
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


@dataclass
class _TemplateIndex:
    affix_template: str
    index: int


@unique
class LayerKind(Enum):
    """
    Enumerates layer variants with a payload containing their affix template and parameter index.

    Use the parameter index with a contiguous slice into the relevant part of your parameter
    list that contains the layer kinds in alphabetical order.
    """

    Casing = _TemplateIndex("{}CA", 0)
    ControlValve = _TemplateIndex("{}CV", 1)
    Fitting = _TemplateIndex("{}FT", 2)
    Hydrant = _TemplateIndex("{}HYD", 3)
    ServiceLine = _TemplateIndex("{}SERV", 4)
    Structure = _TemplateIndex("{}STR", 5)
    SystemValve = _TemplateIndex("{}SV", 6)
    WaterMain = _TemplateIndex("000015-WATER-000{}", 7)


def kind(
    layer: arcpy._mp.Layer,  # pyright: ignore [reportGeneralTypeIssues]
) -> Optional[LayerKind]:
    """
    Returns the type of a layer

    Arguments:
        layer (arcpy._mp.Layer): A layer object.

    Returns:
        LayerKind: The kind of layer.
    """
    layer_name = name(layer)
    for pattern, kind in (
        (r"waControlValve", LayerKind.ControlValve),
        (r"waFitting", LayerKind.Fitting),
        (r"waHydrant", LayerKind.Hydrant),
        (r"waServiceLine", LayerKind.ServiceLine),
        (r"waStructure", LayerKind.Structure),
        (r"waSystemValve", LayerKind.SystemValve),
        (r"waWaterMain", LayerKind.WaterMain),
    ):
        if re.compile(pattern).search(layer_name):
            return kind

    return None

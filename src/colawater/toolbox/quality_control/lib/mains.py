"""
Quality control checks relating to water mains.

Examples:
    .. code-block:: python
    
        res = find_nonexistent_assoc_files(wm_layer)
        do_something(res)

    .. code-block:: python
    
        res = find_incorrect_datasources(layer) 
        do_something(res)
"""

from typing import Optional

import arcpy

import colawater.lib.desc as ly
import colawater.lib.scan as scan
from colawater.lib.error import fallible


@fallible
def find_faulty_scans(
    wm_layer: arcpy._mp.Layer,  # pyright: ignore [reportAttributeAccessIssue]
) -> list[tuple[Optional[str], ...]]:
    """
    Returns a list of object ID and nonexistent scan pairs for the integrated mains in the water main layer.

    Arguments:
        wm_layer (arpcy._mp.Layer): The water main layer.

    Returns:
        list[tuple[str, str]: The list of object ID and comment field tuples.

    Raises:
        ExecuteError: An error ocurred in the tool execution.
    """
    return [
        tuple(i)
        for i in arcpy.da.SearchCursor(  # pyright: ignore [reportAttributeAccessIssue]
            ly.full_path(wm_layer.value),
            ("OBJECTID", "COMMENTS"),
            "INTEGRATIONSTATUS = 'Y'",
        )
        if not scan.exists(i[1])
    ]


@fallible
def find_unknown_datasources(
    wm_layer: arcpy._mp.Layer,  # pyright: ignore [reportAttributeAccessIssue]
) -> list[tuple[Optional[str], ...]]:
    """
    Returns a list of object ID and unknown/null datasource pairs for the integrated mains in the water main layer.

    Arguments:
        wm_layer (arpcy._mp.Layer): The water main layer.

    Returns:
        list[tuple[str, str]]: A list of Object ID and data source field tuples corresponding to water mains from the layer.

    Raises:
        ExecuteError: An error ocurred in the tool execution.
    """
    return [
        tuple(i)
        for i in arcpy.da.SearchCursor(  # pyright: ignore [reportAttributeAccessIssue]
            ly.full_path(wm_layer.value),
            ("OBJECTID", "DATASOURCE"),
            "INTEGRATIONSTATUS = 'Y' AND (DATASOURCE = 'UNK' OR DATASOURCE = '' OR DATASOURCE IS NULL)",
        )
    ]

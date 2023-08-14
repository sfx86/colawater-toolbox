"""
Quality control checks relating to water mains.
"""

from functools import partial

import arcpy

import colawater.attribute as attr
import colawater.layer as ly
import colawater.scan as scan
from colawater.error import fallible


@fallible
def find_nonexistent_assoc_files(
    wm_layer: arcpy._mp.Layer,  # pyright: ignore [reportGeneralTypeIssues]
) -> list[tuple[str, ...]]:
    """
    Returns a list of object ID and nonexistent associated file pairs for the integrated mains
    in the given water main layer.

    Arguments:
        wm_layer (arpcy._mp.Layer): The water main layer.

    Returns:
        list[tuple[str, str]: The list of object ID and comment field tuples.

    Raises:
        ExecuteError: An error ocurred in the tool execution.
    """
    process = partial(attr.process, csv=True)
    return [
        tuple(map(process, i))
        for i in arcpy.da.SearchCursor(  # pyright: ignore [reportGeneralTypeIssues]
            ly.get_path(wm_layer.value),
            ("OBJECTID", "COMMENTS"),
            "INTEGRATIONSTATUS = 'Y'",
        )
        if not scan.exists(i[1])
    ]


@fallible
def find_incorrect_datasources(
    wm_layer: arcpy._mp.Layer,  # pyright: ignore [reportGeneralTypeIssues]
) -> list[tuple[str, ...]]:
    """
    Returns a list of object ID and incorrect data source pairs for the integrated mains
    in the given water main layer.

    Arguments:
        wm_layer (arpcy._mp.Layer): The water main layer.

    Returns:
        list[tuple[str, str]]: A list of Object ID and data source field tuples corresponding
                               to water mains from the layer.

    Raises:
        ExecuteError: An error ocurred in the tool execution.
    """
    process = partial(attr.process, csv=True)
    return [
        tuple(map(process, i))
        for i in arcpy.da.SearchCursor(  # pyright: ignore [reportGeneralTypeIssues]
            ly.get_path(wm_layer.value),
            ("OBJECTID", "DATASOURCE"),
            "INTEGRATIONSTATUS = 'Y' AND (DATASOURCE = 'UNK' OR DATASOURCE = '' OR DATASOURCE IS NULL)",
        )
    ]

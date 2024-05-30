"""
Quality control checks relating to facility identifiers.

Examples:
    .. code-block:: python
    
        res = find_incorrect_fids(layer, re.compile(r"^\\d+example$"))
        do_something(res)

    .. code-block:: python
    
        res = find_duplicate_fids(layer) 
        do_something(res)
"""

import re
from datetime import datetime
from typing import Any, Optional

import arcpy

import colawater.lib.desc as ly
from colawater.lib.error import fallible


@fallible
def find_faulty(
    layer: arcpy._mp.Layer,  # pyright: ignore [reportAttributeAccessIssue]
    regex: re.Pattern[Any],
) -> list[tuple[str, Optional[str]]]:
    """
    Returns all incorrectly formatted facility identifiers matching a regular expression.

    Arguments:
        layer (arcpy._mp.Layer): The layer to check.
        regex (re.Pattern[Any]): The regular expression to match against.

    Returns:
        list[tuple[str, str]]: The list of object IDs and incorrectly formatted facility identifiers.

    Raises:
        ExecuteError: An error ocurred in the tool execution.
    """
    return [
        (str(oid), fid)
        for oid, fid in arcpy.da.SearchCursor(  # pyright: ignore [reportAttributeAccessIssue]
            ly.full_path(layer), ("OBJECTID", "FACILITYID")
        )
        if not regex.fullmatch(str(fid))
    ]


@fallible
def find_duplicate(
    layer: arcpy._mp.Layer,  # pyright: ignore [reportAttributeAccessIssue]
) -> list[tuple[str, ...]]:
    """
    Returns all duplicate facility identifiers from the given layer.

    Arguments:
        layer (arcpy._mp.Layer): The layer to check.

    Returns:
        list[tuple[str, ...]]: The list of object IDs of duplicates, grouped by duplicate values at the zeroth index.

    Raises:
        ExecuteError: An error ocurred in the tool execution.

    Note:
        Writes result layer from ``Find Identical`` into scratch geodatabase.
    """
    scratch_gdb = arcpy.env.scratchGDB  # pyright: ignore [reportAttributeAccessIssue]
    timestamp = datetime.now().strftime("%Y%m%dT%H%M%S")
    scratch_layer_path = f"{scratch_gdb}\\duplicate_fids_{timestamp}"
    layer_path = ly.full_path(layer)

    oids: tuple[int, ...] = tuple(
        int(oid[0])
        for oid in arcpy.da.SearchCursor(  # pyright: ignore [reportAttributeAccessIssue]
            arcpy.management.FindIdentical(  # pyright: ignore [reportAttributeAccessIssue]
                layer_path,
                scratch_layer_path,
                ("FACILITYID"),
                output_record_option="ONLY_DUPLICATES",
            ).getOutput(
                0
            ),
            ("IN_FID"),
        )
    )

    if not oids:
        return []

    oid_to_fid: dict[int, str] = dict(
        arcpy.da.SearchCursor(  # pyright: ignore [reportAttributeAccessIssue]
            layer_path,
            ("OBJECTID", "FACILITYID"),
            where_clause=f"OBJECTID IN ({', '.join(map(str, oids))})",
        )
    )

    duplicates = [tuple(map(str, (oid_to_fid[oid], oid))) for oid in oids]

    return duplicates

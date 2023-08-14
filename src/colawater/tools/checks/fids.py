"""
Quality control checks relating to facility identifiers.
"""

import re
from collections.abc import Generator
from datetime import datetime
from typing import Any

import arcpy

import colawater.attribute as attr
import colawater.layer as ly
from colawater.error import fallible


@fallible
def find_incorrect_fids(
    layer: arcpy._mp.Layer,  # pyright: ignore [reportGeneralTypeIssues]
    regex: re.Pattern[Any],
) -> list[tuple[str, str]]:
    """
    Returns all incorrectly formatted facility identifiers from the given layer
    matching the given regular expression.

    Arguments:
        layer (arcpy._mp.Layer): The layer to check.
        regex (re.Pattern[Any]): The regular expression to match against the facility identifiers in the layer.

    Returns:
        list[tuple[str, str]]: The list of object IDs and incorrectly formatted facility identifiers.

    Raises:
        ExecuteError: An error ocurred in the tool execution.
    """
    return [
        (str(oid), fid_proc)
        for oid, fid in arcpy.da.SearchCursor(  # pyright: ignore [reportGeneralTypeIssues]
            ly.get_path(layer), ("OBJECTID", "FACILITYID")
        )
        if not regex.fullmatch(fid_proc := attr.process(fid))
    ]


@fallible
def find_duplicate_fids(
    layer: arcpy.Parameter,
) -> list[tuple[str, ...]]:
    """
    Returns all duplicate facility identifiers from the given layer.

    Arguments:
        layer (arcpy.Parameter): The layer parameter to check.

    Returns:
        list[tuple[str, ...]]: The list of object IDs of duplicates, grouped by duplicate value, which is at the zeroth index.

    Raises:
        ExecuteError: An error ocurred in the tool execution.

    Note:
        Side effect: Writes result layer into scratch geodatabase.
    """
    scratch_gdb = arcpy.env.scratchGDB  # pyright: ignore [reportGeneralTypeIssues]
    timestamp = datetime.now().strftime("%Y%m%dT%H%M%S")
    scratch_layer_path = f"{scratch_gdb}\\{layer.name}_dup_fids_{timestamp}"
    layer_path = ly.get_path(layer.value)
    # turn very unhelpfully structured result of FindIdentical into
    # oids that were identified as duplicates
    oids: tuple[int, ...] = tuple(
        int(oid[0])
        for oid in arcpy.da.SearchCursor(  # pyright: ignore [reportGeneralTypeIssues]
            arcpy.management.FindIdentical(  # pyright: ignore [reportGeneralTypeIssues]
                layer_path,
                scratch_layer_path,
                ("FACILITYID"),
                output_record_option="ONLY_DUPLICATES",
            ).getOutput(0),
            ("IN_FID"),
        )
    )
    # build comma separated string of oids for SQL query
    if not (oid_str := ", ".join(map(str, oids))):
        return [()]
    # oid to fid mapping to generate more helpful group keys
    oid_to_fid: dict[int, str] = dict(
        arcpy.da.SearchCursor(  # pyright: ignore [reportGeneralTypeIssues]
            layer_path,
            ("OBJECTID", "FACILITYID"),
            where_clause=f"OBJECTID IN ({oid_str})",
        )
    )
    # sorted fid group pairs
    duplicates = [tuple((oid_to_fid[oid], str(oid))) for oid in oids]

    return duplicates

import re
from datetime import datetime
from itertools import groupby
from typing import Any

import arcpy

import colawater.attribute as attr
import colawater.layer as ly
from colawater.error import fallible


@fallible
def find_incorrect_fids(
    layer: arcpy._mp.Layer,  # type: ignore
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
        for oid, fid in arcpy.da.SearchCursor(  # type: ignore
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
    scratch_gdb = arcpy.env.scratchGDB  # type: ignore
    timestamp = datetime.now().strftime("%Y%m%dT%H%M%S")
    scratch_layer_path = f"{scratch_gdb}\\{layer.name}_dup_fids_{timestamp}"
    layer_path = ly.get_path(layer.value)
    # turn very unhelpfully structured result of FindIdentical into
    # list of oids that were identified as duplicates
    oids: list[int] = [
        oid
        for oid, _ in arcpy.da.SearchCursor(  # type: ignore
            arcpy.management.FindIdentical(  # type: ignore
                layer_path,
                scratch_layer_path,
                "FACILITYID",
                output_record_option="ONLY_DUPLICATES",
            ).getOutput(0),
            ("IN_FID", "FEAT_SEQ"),
        )
    ]
    # build comma separated string of oids for SQL query
    if not (oid_str := ", ".join(map(str, oids))):
        return [()]
    # oid to fid mapping to generate more helpful group keys
    oid_to_fid: dict[int, str] = dict(
        arcpy.da.SearchCursor(  # type: ignore
            layer_path,
            ("OBJECTID", "FACILITYID"),
            where_clause=f"OBJECTID IN ({oid_str})",
        )
    )
    # sorted fid group pairs
    fid_group_pairs = sorted(
        [tuple([oid_to_fid[oid], oid]) for oid in oids],
        key=lambda l: l[0],  # type: ignore [arg-type, return-value]
    )
    # list of list of identical groups with fid key as zeroth index
    duplicates = [
        tuple([str(group), *(str(i[1]) for i in data)])
        for group, data in groupby(fid_group_pairs, lambda l: l[0])
    ]

    return duplicates

"""
Contains the functions used by the Water Quality Control tool 
tool and other helper functions.
"""

import re
from collections.abc import Sequence
from typing import Optional

import arcpy

import colawater.attribute as attr
import colawater.status.progressor as pg
import colawater.status.summary as sy
from colawater.tools.checks import fids, mains

_LAYER_START = 4


def execute(parameters: list[arcpy.Parameter]) -> None:
    """
    Entry point for Water Quality Control.

    Arguments:
        parameters (list[arcpy.Parameter]): The list of parameters.
    """
    pg.set_progressor("default", "Starting quality control checks...")

    is_checks = parameters[:_LAYER_START]
    layers = parameters[_LAYER_START:]
    wm_layer = layers[-1]
    is_fid_format_check = is_checks[0].value
    is_fid_duplicate_check = is_checks[1].value
    is_wm_file_check = is_checks[2].value
    is_wm_ds_check = is_checks[3].value

    if is_fid_format_check or is_fid_duplicate_check:
        for l in (l for l in layers if not l.value):
            arcpy.AddWarning(f"Layer omitted: {l.displayName}")

    if is_fid_format_check:
        regexes = (
            r"^\d+CA$",
            r"^\d+CV$",
            r"^\d+FT$",
            r"^\d+HYD$",
            r"^\d+SERV$",
            r"^\d+STR$",
            r"^\d+SV$",
            r"^000015-WATER-000\d+$",
        )

        for l, r in ((l, r) for l, r in zip(layers, regexes) if l.value):
            inc_fids = fids.find_incorrect_fids(l, re.compile(r))

            _boilerplate(
                l.valueAsText,
                "Incorrectly formatted facility identifiers (object ID, facility identifier):",
                inc_fids,
                "incorrectly formatted facility identifiers.",
            )

    if is_fid_duplicate_check:
        for l in (l for l in layers if l.value):
            duplicate_fids = fids.find_duplicate_fids(l.value)

            _boilerplate(
                l.valueAsText,
                "Duplicate facility identifiers grouped on each line (fid, object IDs):",
                duplicate_fids,
                "duplicate facility identifiers.",
                unique=True,
                result_unique_str="unique duplicate facility identifiers.",
            )

    if (is_wm_file_check or is_wm_ds_check) and not wm_layer.value:
        arcpy.AddWarning(
            f"Layer omitted: {wm_layer.displayName}, skipping water main checks."
        )
        return

    if is_wm_file_check:
        nonexistent_files = mains.find_nonexistent_assoc_files(wm_layer)

        _boilerplate(
            wm_layer.valueAsText,
            "Nonexistent associated files (object ID, comments):",
            nonexistent_files,
            "nonexistent files for integrated mains.",
            csv=True,
            unique=True,
            unique_idx=1,
            result_unique_str="unique nonexistent files for integrated mains.",
        )

    if is_wm_ds_check:
        inc_datasources = mains.find_incorrect_datasources(wm_layer)

        _boilerplate(
            wm_layer.valueAsText,
            "Missing or unknown data sources (object ID, datasource):",
            inc_datasources,
            "missing or unknown data sources for integrated mains.",
        )

    sy.post()


def parameters() -> list[arcpy.Parameter]:
    """
    Returns the parameters for Water Quality Control.

    Parameters are 3 of type GPBoolean and 7 of type GPFeatureLayer.

    Returns:
        list[arcpy.Parameter]: The list of parameters.
    """
    checks = [
        arcpy.Parameter(
            displayName=name,
            name=abbrev,
            datatype="GPBoolean",
            parameterType="Optional",
            direction="Input",
        )
        for abbrev, name in (
            # make sure to increment LAYER_START if adding a check here
            ("fid_check", "Check facility identifier format"),
            ("fid_duplicate_check", "Check for duplicate facility identifiers"),
            ("wm_file_check", "Check water main files"),
            ("wm_datasource_check", "Check water main data sources"),
        )
    ]

    lyrs = [
        arcpy.Parameter(
            displayName=name,
            name=abbrev,
            datatype="GPFeatureLayer",
            parameterType="Optional",
            direction="Input",
        )
        for abbrev, name in (
            ("ca_lyr", "Casing"),
            ("cv_lyr", "Control Valve"),
            ("ft_lyr", "Fitting"),
            ("hy_lyr", "Hydrant"),
            ("sl_lyr", "Service Line"),
            ("st_lyr", "Structure"),
            ("sv_lyr", "System Valve"),
            ("wm_lyr", "Water Main"),
        )
    ]

    return [*checks, *lyrs]


def _boilerplate(
    layer_name: str,
    result_header_str: str,
    items: Sequence[Sequence[Optional[str]]],
    result_total_str: str,
    csv: bool = False,
    unique: bool = False,
    unique_idx: int = 0,
    result_unique_str: str = "",
) -> None:
    if items:
        sy.add_result(layer_name, result_header_str)
        if csv:
            sy.add_note(layer_name, attr.CSV_PROCESSING_MSG)
        sy.add_items(items, csv=csv)

    sy.add_result(layer_name, f"{len(items):n} {result_total_str}")

    if unique and (items and items[0]):
        sy.add_result(
            layer_name,
            f"{len(set(i[unique_idx] for  i in items)):n} {result_unique_str}",
        )

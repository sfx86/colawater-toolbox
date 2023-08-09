"""
Contains the functions used by the Water Quality Control tool 
tool and other helper functions.
"""

import re
from typing import Any

import arcpy

import colawater.attribute as attr
import colawater.layer as ly
import colawater.status.logging as log
import colawater.status.progressor as pg
import colawater.status.summary as sy
from colawater import scan
from colawater.error import fallible

_LAYER_START = 3


def execute(parameters: list[arcpy.Parameter]) -> None:
    """
    Entry point for Water Quality Control.

    Raises:
        ExecuteError: An error ocurred in the tool execution.
    """
    pg.set_progressor("default", "Starting quality control checks...")

    checks = parameters[:_LAYER_START]
    layers = parameters[_LAYER_START:]
    wm_layer = layers[-1]
    is_fid_format_check = checks[0].value
    is_wm_file_check = checks[1].value
    is_wm_ds_check = checks[2].value

    _add_csv_msg = lambda s: sy.add_note(s, attr.CSV_PROCESSING_MSG)
    _log_layer_with_info = lambda l, s: log.info(f"[{l}] {s}")

    if is_fid_format_check:
        pg.set_progressor("step", "Validating facility identifiers...", 0, 7)
        # regexes correspond 1:1 with layer parameters
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

        for l, r in zip(layers, regexes):
            # guard against None
            if not l.value:
                log.warning(f"Layer omitted: {l.displayName}")
                pg.increment()
                continue

            _log_layer_with_info(
                l.valueAsText, "Checking facility identifier formatting..."
            )

            inc_fids = _find_incorrect_fids(l, re.compile(r))

            pg.increment()
            sy.add_result(
                l.valueAsText,
                "Incorrectly formatted facility identifiers (object ID, facility identifier):",
            )
            _add_csv_msg(wm_layer.valueAsText)
            sy.add_items(inc_fids, csv=True)
            sy.add_result(
                l.valueAsText,
                f"{len(inc_fids):n} incorrectly formatted facility identifiers.",
            )

    if not wm_layer.value:
        log.warning(
            f"Layer omitted: {wm_layer.displayName}, skipping water main checks."
        )
        return

    pg.set_progressor("default")

    if is_wm_file_check:
        _log_layer_with_info(
            wm_layer.valueAsText, "Verifying assiociated files for integrated mains..."
        )

        nonexistent_files = _find_nonexistent_assoc_files(wm_layer)

        sy.add_result(
            wm_layer.valueAsText, "Nonexistent associated files (object ID, comments):"
        )
        _add_csv_msg(wm_layer.valueAsText)
        sy.add_items(nonexistent_files, csv=True)
        sy.add_result(
            wm_layer.valueAsText,
            f"{len(nonexistent_files):n} nonexistent files for integrated mains.",
        )
        num_unique = len({list[1] for list in nonexistent_files})
        sy.add_result(
            wm_layer.valueAsText,
            f"{num_unique:n} unique nonexistent files files for integrated mains.",
        )

    if is_wm_ds_check:
        _log_layer_with_info(
            wm_layer.valueAsText, "Checking data sources for integrated mains..."
        )

        inc_datasources = _find_incorrect_datasources(wm_layer)

        sy.add_result(
            wm_layer.valueAsText,
            "Missing or unknown data sources (object ID, datasource):",
        )
        _add_csv_msg(wm_layer.valueAsText)
        sy.add_items(inc_datasources, csv=True)
        sy.add_result(
            wm_layer.valueAsText,
            f"{len(inc_datasources):n} missing or unknown data sources for integrated mains.",
        )

    # TODO: deduplication
    # TODO: domain conformation

    sy.post()


def parameters() -> list[arcpy.Parameter]:
    """
    Returns the parameters for Water Quality Control.

    Parameters are 3 of type GPBoolean and 7 of type GPFeatureLayer.

    Returns:
        list[arcpy.Parameter]: The list of parameters.
    """
    check_templates = (
        # make sure to increment LAYER_START if adding a check here
        ("fid_check", "Check facility identifiers"),
        ("wm_file_check", "Check water main files"),
        ("wm_datasource_check", "Check water main data sources"),
    )

    checks = [
        arcpy.Parameter(
            displayName=name,
            name=abbrev,
            datatype="GPBoolean",
            parameterType="Optional",
            direction="Input",
        )
        for abbrev, name in check_templates
    ]

    lyr_templates = (
        ("ca_lyr", "Casing"),
        ("cv_lyr", "Control Valve"),
        ("ft_lyr", "Fitting"),
        ("hy_lyr", "Hydrant"),
        ("sl_lyr", "Service Line"),
        ("st_lyr", "Structure"),
        ("sv_lyr", "System Valve"),
        ("wm_lyr", "Water Main"),
    )

    lyrs = [
        arcpy.Parameter(
            displayName=name,
            name=abbrev,
            datatype="GPFeatureLayer",
            parameterType="Optional",
            direction="Input",
        )
        for abbrev, name in lyr_templates
    ]

    return [*checks, *lyrs]


@fallible
def _find_incorrect_fids(
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
        list[str]: The list of incorrectly formatted facility identifiers.

    Raises:
        ExecuteError: An error ocurred in the tool execution.
    """
    with arcpy.da.SearchCursor(  # type: ignore
        ly.get_path(layer), ("OBJECTID", "FACILITYID")
    ) as cursor:
        inc_fids = [
            (oid, fid_proc)
            for oid, fid in cursor
            if not regex.fullmatch(fid_proc := attr.process(fid))
        ]

    return inc_fids


@fallible
def _find_nonexistent_assoc_files(
    wm_layer: arcpy._mp.Layer,  # type: ignore
) -> list[tuple[str, str]]:
    """
    Returns a list of object ID and nonexistent associated file pairs for the integrated mains
    in the given water main layer.

    Arguments:
        wm_layer (arpcy._mp.Layer): The water main layer.

    Returns:
        list[tuple[str, str]: A list of Object ID and comment field tuples corresponding to water mains from the layer.

    Raises:
        ExecuteError: An error ocurred in the tool execution.
    """
    with arcpy.da.SearchCursor(  # type: ignore
        ly.get_path(wm_layer.value),
        ("OBJECTID", "COMMENTS"),
        "INTEGRATIONSTATUS = 'Y'",
    ) as cursor:
        nonexistent_files = [
            (oid, attr.process(comments))
            for oid, comments in cursor
            if scan.exists(comments)
        ]

    return nonexistent_files


@fallible
def _find_incorrect_datasources(
    wm_layer: arcpy._mp.Layer,  # type: ignore
) -> list[tuple[str, str]]:
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
    with arcpy.da.SearchCursor(  # type: ignore
        ly.get_path(wm_layer.value),
        ("OBJECTID", "DATASOURCE"),
        "INTEGRATIONSTATUS = 'Y' AND (DATASOURCE = 'UNK' OR DATASOURCE = '' OR DATASOURCE IS NULL)",
    ) as cursor:
        inc_datasources = [
            (oid, attr.process(datasource)) for oid, datasource in cursor
        ]

    return inc_datasources

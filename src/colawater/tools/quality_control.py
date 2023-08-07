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
    arcpy.SetProgressor("default", "Starting quality control checks...")

    checks = parameters[:_LAYER_START]
    layers = parameters[_LAYER_START:]
    wm_layer = layers[-1]
    is_fid_format_check = checks[0].value
    is_wm_file_check = checks[1].value
    is_wm_ds_check = checks[2].value

    if is_fid_format_check:
        arcpy.SetProgressor("step", "Validating facility identifiers...", 0, 7)
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

            log.info(f"Searching in [{l.valueAsText}]...")

            inc_fids = _find_incorrect_fids(l, r)

            pg.increment()
            sy.add_result(
                l.valueAsText,
                "Incorrectly formatted facility identifiers (object ID, facility identifier):",
            )

            for i in inc_fids:
                sy.add_item(", ".join(i))

            sy.add_result(
                l.valueAsText,
                f"{len(inc_fids):n} incorrectly formatted facility identifiers.",
            )

    if not wm_layer.value:
        log.warning(
            f"Layer omitted: {wm_layer.valueAsText}, skipping water main checks."
        )
        return

    arcpy.SetProgressor("default")

    if is_wm_file_check:
        pg.label("Verifying assiociated files for integrated mains...")

        nonexistent_files = _find_nonexistent_assoc_files(wm_layer)

        sy.add_result(
            wm_layer.valueAsText, "Nonexistent associated files (object ID, comments):"
        )
        sy.add_note(wm_layer.valueAsText, attr.CSV_PROCESSING_MSG)

        for oid, file in nonexistent_files:
            sy.add_item(", ".join((oid, attr.process(file, csv=True))))

        sy.add_result(
            wm_layer.valueAsText,
            f"{len(nonexistent_files):n} nonexistent files for integrated mains.",
        )
        sy.add_result(
            wm_layer.valueAsText,
            f"{len(set(nonexistent_files)):n} unique nonexistent files files for integrated mains.",
        )

    if is_wm_ds_check:
        log.info(
            f"Verifying data sources for integrated mains in [{wm_layer.valueAsText}]..."
        )

        inc_datasources = _find_incorrect_datasources(wm_layer)

        sy.add_result(
            wm_layer.valueAsText,
            "Missing or unknown data sources (object ID, datasource):",
        )

        for i in inc_datasources:
            sy.add_item(", ".join(i))

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
        regex (re.Pattern[Any]): The regular expression to use to check the facility
                                 identifiers in the layer.

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
        list[tuple[str, str]: A list of Object ID and comment field tuples corresponding
                              to water mains from the layer.

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

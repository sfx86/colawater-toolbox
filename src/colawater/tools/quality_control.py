"""
Contains the functions used by the Water Quality Control tool 
tool and other helper functions.
"""

import arcpy
import re
from colawater.utils.status import StatusUpdater
from colawater.utils.summary import SummaryCollection
from colawater.utils.functions import get_layer_path, is_existing_scan, process_attr
from colawater.utils.constants import CSV_PROCESSING_MSG, RUNTIME_ERROR_MSG
from typing import Sequence


def execute(parameters: list[arcpy.Parameter]) -> None:
    """
    Entry point for Water Quality Control.

    Raises:
        ExecutionError: An error ocurred in the tool execution.
    """
    arcpy.SetProgressor("default", "Starting quality control checks...")
    status = StatusUpdater()
    # functions are coupled to these keys,
    # they don't check to make sure they exist
    # beware of KeyErrors
    summaries = SummaryCollection(["fid_format", "wm_file", "wm_datasource"])

    LAYER_START = 3
    checks = parameters[:LAYER_START]
    lyrs = parameters[LAYER_START:]
    lyr_wm = lyrs[-1]
    is_fid_format_check = checks[0].value
    is_wm_file_check = checks[1].value
    is_wm_ds_check = checks[2].value

    if is_fid_format_check:
        # regexes correspond 1:1 with layer parameters
        regexes = (
            re.compile(r"^\d+CA$"),
            re.compile(r"^\d+CV$"),
            re.compile(r"^\d+FT$"),
            re.compile(r"^\d+HYD$"),
            re.compile(r"^\d+SERV$"),
            re.compile(r"^\d+STR$"),
            re.compile(r"^\d+SV$"),
            re.compile(r"^000015-WATER-000\d+$"),
        )
        _fid_format_qc(lyrs, regexes, status, summaries)

    if is_wm_file_check:
        _wm_assoc_file_qc(lyr_wm, status, summaries)

    if is_wm_ds_check:
        _wm_datasource_qc(lyr_wm, status, summaries)

    # TODO: deduplication
    # TODO: domain conformation

    summaries.post()


def post_execute(parameters: list[arcpy.Parameter]) -> None:
    """
    Note:
        Unimplemented for this tool.
    """
    pass


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


def update_parameters(parameters: list[arcpy.Parameter]) -> None:
    """
    Note:
        Unimplemented for this tool.
    """
    pass


def update_messages(parameters: list[arcpy.Parameter]) -> None:
    """
    Note:
        Unimplemented for this tool.
    """
    pass


def _fid_format_qc(
    layers: list[arcpy._mp.Layer],
    regexes: Sequence[re.Pattern],
    status: StatusUpdater,
    summaries: SummaryCollection,
) -> None:
    """
    Finds all incorrectly formatted facility identifiers.

    Arguments:
        layers (list[arcpy._mp.Layer]): List of layers to check.
        regexes (list[re.Pattern]): List of regexes to use to check the layers'
                                    facility identifiers.
        status (StatusUpdater): The status for this tool.
        summaries (SummaryCollection): The summaries for this tool.

    Raises:
        ExecutionError: An error ocurred in the tool execution.

    Note:
        ``layers`` and ``regexes`` should correspond 1:1; otherwise,
        the check will stop when the shortest list is exhausted.
    """
    arcpy.SetProgressor("step", "Validating facility identifiers...", 0, 7)

    for l, r in zip(layers, regexes):
        lyr = l.value
        lyr_name = l.displayName

        # guard against None
        if not lyr:
            status.update_warn(f"Layer omitted: {lyr_name}")
            continue

        fields = ("OBJECTID", "FACILITYID")
        lyr_name_long = l.valueAsText
        lyr_path = get_layer_path(lyr)
        num_no_match = 0

        status.update_info(
            f"Finding incorrectly formatted facility identifiers in [{lyr_name_long}]..."
        )

        try:
            with arcpy.da.SearchCursor(lyr_path, fields) as cursor:
                summaries.items["fid_format"].add_result(
                    lyr_name_long,
                    "Incorrectly formatted facility identifiers (object ID, facility identifier):",
                )
                summaries.items["fid_format"].add_note(
                    lyr_name_long, CSV_PROCESSING_MSG
                )
                for row in cursor:
                    oid = row[0]
                    fid = process_attr(row[1], csv=True)
                    if not r.fullmatch(fid):
                        summaries.items["fid_format"].add_item(f"{oid}, {fid}")
                        num_no_match += 1
        # arcpy should only ever throw RuntimeError here, but you never know
        except Exception:
            # post existing summaries as to not lose information
            summaries.post(dumped=True)
            status.update_err(RUNTIME_ERROR_MSG)
        summaries.items["fid_format"].add_result(
            lyr_name_long,
            f"{num_no_match:n} incorrectly formatted facility identifiers.",
        )


def _wm_assoc_file_qc(
    water_main_layer: arcpy._mp.Layer,
    status: StatusUpdater,
    summaries: SummaryCollection,
) -> None:
    """
    Verifies that each integrated main has an associated file that exists.

    Arguments:
        water_main_layer (arpcy._mp.Layer): The water main layer.
        status (StatusUpdater): The status for this tool.
        summaries (SummaryCollection): The summaries for this tool.

    Raises:
        ExecutionError: An error ocurred in the tool execution.
    """
    arcpy.SetProgressor(
        "default", "Verifying assiociated files for integrated mains..."
    )

    lyr = water_main_layer.value
    lyr_name = water_main_layer.displayName
    lyr_name_long = water_main_layer.valueAsText

    status.update_info(
        f"Verifying associated file exists for integrated mains in [{lyr_name_long}]...",
        increment=False,
    )

    # guard against None
    if not lyr:
        status.update_warn(f"Layer omitted: {lyr_name}", increment=False)
        return

    fields = ("OBJECTID", "COMMENTS")
    lyr_path = get_layer_path(lyr)
    num_not_exists = 0
    num_exists = 0
    unique_comments = set()
    where_integrated = "INTEGRATIONSTATUS = 'Y'"

    summaries.items["wm_file"].add_result(
        lyr_name_long, "Non-existant associated files (object ID, comments):"
    )
    summaries.items["wm_file"].add_note(lyr_name_long, CSV_PROCESSING_MSG)

    try:
        with arcpy.da.SearchCursor(lyr_path, fields, where_integrated) as cursor:
            for row in cursor:
                oid = row[0]
                comments = process_attr(row[1], csv=True)
                unique_comments.add(comments)

                if comments == "<Null>":
                    summaries.items["wm_file"].add_item(f"{oid}, {comments}")
                    num_not_exists += 1
                    continue

                if is_existing_scan(comments):
                    num_exists += 1
                else:
                    summaries.items["wm_file"].add_item(f"{oid}, {comments}")
                    num_not_exists += 1
                # there's so many files that the progressor only needs updating
                # every couple of files
                # the progressor queues the updates anyways,
                # so might as well not hit it as often
                # ~3k files per second, so (total mod 1500) will update ~2x/s
                if (num_exists + num_not_exists) % 1500 == 0:
                    status.update_label(
                        f"Associated file count (existant : non-existant): {num_exists:>9n} : {num_not_exists:<9n}"
                    )
    # arcpy should only ever throw RuntimeError here, but you never know
    except Exception:
        # post existing summaries as to not lose information
        summaries.post(dumped=True)
        status.update_err(RUNTIME_ERROR_MSG)

    summaries.items["wm_file"].add_result(
        lyr_name_long,
        f"{num_exists:n} existant and {num_not_exists:} non-existant files for integrated mains.",
    )
    summaries.items["wm_file"].add_result(
        lyr_name_long,
        f"{len(unique_comments):n} unique non-existant files files for integrated mains.",
    )
    summaries.items["wm_file"].add_result(
        lyr_name_long,
        f"{num_exists + num_not_exists:n} total files checked for integrated mains.",
    )


def _wm_datasource_qc(
    water_main_layer: arcpy._mp.Layer,
    status: StatusUpdater,
    summaries: SummaryCollection,
) -> None:
    """
    Verifies that each integrated main's data source is set and not Unknown.

    Arguments:
        water_main_layer (arpcy._mp.Layer): The water main layer.
        status (StatusUpdater): The status for this tool.
        summaries (SummaryCollection): The summaries for this tool.

    Raises:
        ExecutionError: An error ocurred in the tool execution.
    """
    arcpy.SetProgressor("step", "Validating facility identifiers...", 0, 7)

    lyr = water_main_layer.value
    lyr_name = water_main_layer.displayName
    lyr_name_long = water_main_layer.valueAsText

    status.update_info(
        f"Verifying data sources for integrated mains in [{lyr_name_long}]..."
    )

    # guard against None
    if not lyr:
        status.update_warn(f"Layer omitted: {lyr_name}")
        return

    fields = ("OBJECTID", "DATASOURCE")
    lyr_path = get_layer_path(lyr)
    num_missing_unk = 0
    where_wrong = "INTEGRATIONSTATUS = 'Y' AND (DATASOURCE = 'UNK' OR DATASOURCE = '' OR DATASOURCE IS NULL)"

    summaries.items["wm_datasource"].add_result(
        lyr_name_long, "Missing or unknown data sources (object ID, datasource):"
    )
    summaries.items["wm_datasource"].add_note(lyr_name_long, CSV_PROCESSING_MSG)

    try:
        with arcpy.da.SearchCursor(lyr_path, fields, where_wrong) as cursor:
            for row in cursor:
                oid = row[0]
                datasource = process_attr(row[1], csv=True)
                summaries.items["wm_datasource"].add_item(f"{oid}, {datasource}")
                num_missing_unk += 1
    # arcpy should only ever throw RuntimeError here, but you never know
    except Exception:
        # post existing summaries as to not lose information
        summaries.post(dumped=True)
        status.update_err(RUNTIME_ERROR_MSG)

    summaries.items["wm_datasource"].add_result(
        lyr_name_long,
        f"{num_missing_unk:n} missing or unknown data sources for integrated mains.",
    )

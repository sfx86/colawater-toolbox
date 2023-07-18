import arcpy
from functools import cache
from pathlib import Path
import re
import utils


def execute(parameters: list[arcpy.Parameter]) -> None:
    """Entry point for Quality Control."""
    arcpy.SetProgressor("default", "Starting quality control checks...")
    status = utils.StatusUpdater()
    summaries = utils.SummaryContainer()
    summaries.add_summaries(["validator", "int_file"])

    checks = parameters[:2]
    lyrs = parameters[2:]
    is_fid_check = checks[0].value
    is_wm_check = checks[1].value

    if is_fid_check:
        _fid_validation_qc(lyrs, status, summaries)

    if is_wm_check:
        _wm_assoc_file_qc(lyrs[-1], status, summaries)

    # TODO: deduplication
    # TODO: domain conformation

    summaries.post()


def post_execute(parameters: list[arcpy.Parameter]) -> None:
    """Unimplemented for this tool."""
    pass


def parameters() -> list[arcpy.Parameter]:
    """Return a list of parameter definitions."""
    check_templates = (
        ("fid_check", "Validate facility identifiers"),
        ("wm_check", "Verify associated files for integrated mains"),
    )

    checks = [
        arcpy.Parameter(
            displayName=disp,
            name=abbrev,
            datatype="GPBoolean",
            parameterType="Optional",
            direction="Input",
        )
        for abbrev, disp in check_templates
    ]

    check_templates = (
        ("ca_lyr", "Casing"),
        ("cv_lyr", "Control Valve"),
        ("ft_lyr", "Fitting"),
        ("hy_lyr", "Hydrant"),
        ("sl_lyr", "Service Line"),
        ("st_lyr", "Structure"),
        ("sv_lyr", "System Valve"),
        ("wm_lyr", "Water Main"),
    )

    layers = [
        arcpy.Parameter(
            displayName=disp,
            name=disp,
            datatype="GPFeatureLayer",
            parameterType="Optional",
            direction="Input",
        )
        for disp, disp in check_templates
    ]

    return [*checks, *layers]


def update_parameters(parameters: list[arcpy.Parameter]) -> None:
    """Unimplemented for this tool."""
    pass


def update_messages(parameters: list[arcpy.Parameter]) -> None:
    """Unimplemented for this tool."""
    pass


def _fid_validation_qc(
    layers: list[arcpy._mp.Layer],
    status: utils.StatusUpdater,
    summaries: utils.SummaryContainer,
) -> None:
    """Finds all non-conforming facility identifiers and generates a report containing them."""
    arcpy.SetProgressor("step", "Validating facility identifiers...", 0, 7)
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

    for l, r in zip(layers, regexes):
        lyr = l.value
        lyr_disp_name = l.displayName

        # guard against None
        if not lyr:
            status.update_warn(f"Layer omitted: {lyr_disp_name}")
            continue

        fields = ("OBJECTID", "FACILITYID")
        lyr_name = l.valueAsText
        lyr_path = utils.get_layer_path(lyr)

        # fid validation
        status.update_info(f"Validating facility identifiers for [{lyr_name}]...")
        try:
            with arcpy.da.SearchCursor(lyr_path, fields) as cursor:
                summaries.validator.add_header(
                    f"[{lyr_name}] Non-conforming facility identifiers (object ID, facility identifier):"
                )
                for row in cursor:
                    oid, fid = row
                    if not r.fullmatch(fid):
                        summaries.validator.add_item(f"{oid}, {fid}")
        # arcpy should only ever throw RuntimeError here, but you never know
        except Exception:
            # post existing summaries as to not lose information
            summaries.post()
            status.update_err(utils.RUNTIME_ERROR_MSG)


def _wm_assoc_file_qc(
    water_main_layer: arcpy._mp.Layer,
    status: utils.StatusUpdater,
    summaries: utils.SummaryContainer,
) -> None:
    """Verifies that each integrated main has an associated file that exists."""
    arcpy.SetProgressor(
        "default", "Verifying assiociated files for integrated mains..."
    )

    lyr = water_main_layer.value
    lyr_name = water_main_layer.valueAsText

    status.update_info(
        f"Verifying associated file exists for integrated mains in [{lyr_name}]...",
        bump=False,
    )

    # guard against None
    if not lyr:
        status.update_warn(f"Layer omitted: {lyr_disp_name}", bump=False)
        return

    fields = ("OBJECTID", "COMMENTS")
    lyr_disp_name = water_main_layer.displayName
    lyr_path = utils.get_layer_path(lyr)
    where_integrated = "INTEGRATIONSTATUS = 'Y'"

    try:
        with arcpy.da.SearchCursor(lyr_path, fields, where_integrated) as cursor:
            summaries.int_file.add_header(
                f"[{lyr_name}] Invalid associated files (object ID, comments):"
            )
            summaries.int_file.add_header(
                f"Note: commas and quotation marks have been removed so this output can be consumed properly as a CSV."
            )
            num_valid = 0
            num_invalid = 0
            for row in cursor:
                oid = row[0]
                comments = row[1]
                # only check for none as empty strings are also falsy and
                # naming those <Null> would cause confusion
                if comments is None:
                    comments = "<Null>"
                    summaries.int_file.add_item(f"{oid}, {comments}")
                    num_invalid += 1
                    continue
                else:
                    # some comments have erroneous whitespace or contain commas or quotes
                    # remove these to make use as csv possible
                    comments = comments.strip().replace(",", "").replace('"', "")
                if _is_valid_file(comments):
                    num_valid += 1
                else:
                    summaries.int_file.add_item(f"{oid}, {comments}")
                    num_invalid += 1
                # there's so many files that the progressor only needs updating
                # every couple of files; the progressor queues the updates
                # anyways, so might as well not hit it as often
                # ~3k files per second, so total mod 1500 will update ~2x/s 
                if (num_valid + num_invalid) % 1500 == 0:
                    arcpy.SetProgressorLabel(
                        f"Associated file count (valid : invalid): {num_valid:>9n} : {num_invalid:<9n}"
                    )
    # arcpy should only ever throw RuntimeError here, but you never know
    except Exception:
        # post existing summaries as to not lose information
        summaries.post()
        status.update_err(utils.RUNTIME_ERROR_MSG)

    summaries.int_file.add_header(
        f"[{lyr_name}] Verified associated files for integrated mains:"
    )
    summaries.int_file.add_item(f"{num_valid:n} valid, {num_invalid:} invalid.")
    summaries.int_file.add_item(f"{num_valid + num_invalid:n} total files checked.")


@cache
def _is_valid_file(filename: str) -> bool:
    """Return true if the given string is a valid scan filename."""
    # takes advantage of short-circuiting to avoid filesystem ops where possible
    # this function is extremely hot and many of the arguments are identical, hence
    # the @cache decorator
    return filename and (
        (
            # valid data sources only ever have these extensions
            filename.endswith(".tif")
            or filename.endswith(".pdf")
            or filename.endswith(".dwg")
        )
        and Path(f"M:\\Util&Eng\\Dept_Staff\\Scans\\{filename}").exists()
    )

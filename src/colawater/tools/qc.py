import arcpy
from colawater import utils
import re


def execute(parameters: list[arcpy.Parameter]) -> None:
    """Entry point for Quality Control."""
    arcpy.SetProgressor("default", "Starting quality control checks...")
    status = utils.StatusUpdater()
    summaries = utils.SummaryContainer(["fid_format", "wm_file", "wm_datasource"])

    LAYER_START = 3
    checks = parameters[:LAYER_START]
    lyrs = parameters[LAYER_START:]
    lyr_wm = lyrs[-1]
    is_fid_format_check = checks[0].value
    is_wm_file_check = checks[1].value
    is_wm_ds_check = checks[2].value

    if is_fid_format_check:
        _fid_format_qc(lyrs, status, summaries)

    if is_wm_file_check:
        _wm_assoc_file_qc(lyr_wm, status, summaries)

    if is_wm_ds_check:
        _wm_datasource_qc(lyr_wm, status, summaries)

    # TODO: deduplication
    # TODO: domain conformation

    summaries.post()


def post_execute(parameters: list[arcpy.Parameter]) -> None:
    """Unimplemented for this tool."""
    pass


def parameters() -> list[arcpy.Parameter]:
    """Return a list of parameter definitions."""
    check_templates = (
        # make sure to increment LAYER_START if adding a check here
        ("fid_check", "Check facility identifiers"),
        ("wm_file_check", "Check water main files"),
        ("wm_datasource_check", "Check water main data sources"),
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

    layers = [
        arcpy.Parameter(
            displayName=disp,
            name=disp,
            datatype="GPFeatureLayer",
            parameterType="Optional",
            direction="Input",
        )
        for disp, disp in lyr_templates
    ]

    return [*checks, *layers]


def update_parameters(parameters: list[arcpy.Parameter]) -> None:
    """Unimplemented for this tool."""
    pass


def update_messages(parameters: list[arcpy.Parameter]) -> None:
    """Unimplemented for this tool."""
    pass


def _fid_format_qc(
    layers: list[arcpy._mp.Layer],
    status: utils.StatusUpdater,
    summaries: utils.SummaryContainer,
) -> None:
    """Finds all incorrectly formatted facility identifiers."""
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

        status.update_info(
            f"Finding incorrectly formatted facility identifiers in [{lyr_name}]..."
        )

        try:
            with arcpy.da.SearchCursor(lyr_path, fields) as cursor:
                summaries.items["fid_format"].add_header(
                    f"[{lyr_name}] Incorrectly formatted facility identifiers (object ID, facility identifier):"
                )
                summaries.items["fid_format"].add_header(utils.CSV_PROCESSING_MSG)
                for row in cursor:
                    oid = row[0]
                    fid = utils.process_attr(row[1], csv=True)
                    if not r.fullmatch(fid):
                        summaries.items["fid_format"].add_item(f"{oid}, {fid}")
        # arcpy should only ever throw RuntimeError here, but you never know
        except Exception:
            # post existing summaries as to not lose information
            summaries.post(dumped=True)
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
    lyr_disp_name = water_main_layer.displayName
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
    lyr_path = utils.get_layer_path(lyr)
    num_not_exists = 0
    num_exists = 0
    unique_comments = set()
    where_integrated = "INTEGRATIONSTATUS = 'Y'"

    summaries.items["wm_file"].add_header(
        f"[{lyr_name}] Non-existant associated files (object ID, comments):"
    )
    summaries.items["wm_file"].add_header(utils.CSV_PROCESSING_MSG)

    try:
        with arcpy.da.SearchCursor(lyr_path, fields, where_integrated) as cursor:
            for row in cursor:
                oid = row[0]
                comments = utils.process_attr(row[1], csv=True)
                unique_comments.add(comments)

                if comments == "<Null>":
                    summaries.items["wm_file"].add_item(f"{oid}, {comments}")
                    num_not_exists += 1
                    continue

                if utils.is_existing_scan(comments):
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
        status.update_err(utils.RUNTIME_ERROR_MSG)

    summaries.items["wm_file"].add_header(
        f"[{lyr_name}] Verified associated files for integrated mains:"
    )
    summaries.items["wm_file"].add_item(
        f"{num_exists:n} existant, {num_not_exists:} non-existant."
    )
    summaries.items["wm_file"].add_item(f"{len(unique_comments):n} unique non-existant files.")
    summaries.items["wm_file"].add_item(f"{num_exists + num_not_exists:n} total files checked.")


def _wm_datasource_qc(
    water_main_layer: arcpy._mp.Layer,
    status: utils.StatusUpdater,
    summaries: utils.SummaryContainer,
) -> None:
    """Verifies that each integrated main's data source is set and not Unknown."""
    arcpy.SetProgressor("default", "Verifying data sources for integrated mains...")

    lyr = water_main_layer.value
    lyr_disp_name = water_main_layer.displayName
    lyr_name = water_main_layer.valueAsText

    status.update_info(
        f"Verifying data sources for integrated mains in [{lyr_name}]...",
        bump=False,
    )

    # guard against None
    if not lyr:
        status.update_warn(f"Layer omitted: {lyr_disp_name}", bump=False)
        return

    fields = ("OBJECTID", "DATASOURCE")
    lyr_path = utils.get_layer_path(lyr)
    num_missing_unk = 0
    where_wrong = "INTEGRATIONSTATUS = 'Y' AND (DATASOURCE = 'UNK' OR DATASOURCE = '' OR DATASOURCE IS NULL)"

    summaries.items["wm_datasource"].add_header(
        f"[{lyr_name}] Missing or unknown data sources (object ID, datasource):"
    )
    summaries.items["wm_datasource"].add_header(utils.CSV_PROCESSING_MSG)

    try:
        with arcpy.da.SearchCursor(lyr_path, fields, where_wrong) as cursor:
            for row in cursor:
                oid = row[0]
                datasource = utils.process_attr(row[1], csv=True)
                summaries.items["wm_datasource"].add_item(f"{oid}, {datasource}")
                num_missing_unk += 1
    # arcpy should only ever throw RuntimeError here, but you never know
    except Exception:
        # post existing summaries as to not lose information
        summaries.post(dumped=True)
        status.update_err(utils.RUNTIME_ERROR_MSG)

    summaries.items["wm_datasource"].add_header(
        f"[{lyr_name}] Missing or unknown data sources for integrated mains:"
    )
    summaries.items["wm_datasource"].add_item(f"{num_missing_unk:n} missing or unknown.")

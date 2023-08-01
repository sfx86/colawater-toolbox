import getpass
from datetime import datetime, timedelta

import arcpy

from colawater.utils.constants import CW2020_SCAN_DIR, RUNTIME_ERROR_MSG, SCAN_DIR
from colawater.utils.functions import get_layer_workspace
from colawater.utils.status import StatusUpdater
from colawater.utils.summary import SummaryBuilder


def execute(parameters: list[arcpy.Parameter]) -> None:
    """
    Entry point for Append to ART.

    Appends recent integrated and well-sourced mains from a given editor to the
    Asset Reference Table.
    It maps the fields like so:

    =========== ==================
    Source      ART Destination
    =========== ==================
    city_file   FILELOCATIONCITY
    DATASOURCE  DRAWINGTYPE
    INSTALLDATE DRAWINGDATE
    FACILIITYID ASSETFACILITYID
    COMMENTS    SCANNAME
    cw2020_file FILELOCATIONCW2020
    =========== ==================

    Raises:
        ExecutionError: An error ocurred in the tool execution.
    """
    arcpy.SetProgressor("default", "Appending mains to ART...")
    status = StatusUpdater()
    summary = SummaryBuilder()

    last_editor = parameters[0].valueAsText
    on_after_date = parameters[1].valueAsText
    wm_lyr = parameters[2]
    wm_lyr_name_long = wm_lyr.valueAsText
    art_table = parameters[3]
    art_table_name_long = art_table.valueAsText
    art_fields = (
        "FILELOCATIONCITY",
        "DRAWINGTYPE",
        "DRAWINGDATE",
        "ASSETFACILITYID",
        "ASSETTYPE",
        "SCANNAME",
        "FILELOCATIONCW2020",
    )
    wm_fields = ("FACILITYID", "INSTALLDATE", "DATASOURCE", "COMMENTS")
    where_water = " ".join(
        (
            "INTEGRATIONSTATUS = 'Y'",
            f"AND LASTEDITOR = '{last_editor}'",
            f"AND LASTUPDATE >= timestamp '{on_after_date}'",
            "AND LIFECYCLESTATUS = 'Active'",
            "AND OWNEDBY = 1",
            "AND (DATASOURCE = 'SURVGPS' OR DATASOURCE = 'ASB')",
        )
    )
    workspace = get_layer_workspace(wm_lyr.value)
    num_appended = 0

    status.update_info(
        f"Appending mains from [{wm_lyr_name_long}] to [{art_table_name_long}]...",
        increment=False,
    )

    try:
        with arcpy.da.Editor(workspace):
            with arcpy.da.SearchCursor(
                wm_lyr.value, wm_fields, where_water
            ) as search_cursor, arcpy.da.InsertCursor(
                art_table.value, art_fields
            ) as insert_cursor:
                for row in search_cursor:
                    fid, install_date, datasource, comments = row
                    asset_type = "WAM"
                    cw2020_file = str(CW2020_SCAN_DIR / comments)
                    city_file = str(SCAN_DIR / comments)
                    row = [
                        city_file,
                        datasource,
                        install_date,
                        fid,
                        asset_type,
                        comments,
                        cw2020_file,
                    ]
                    insert_cursor.insertRow(row)
                    num_appended += 1
    except Exception:
        summary.post()
        status.update_err(RUNTIME_ERROR_MSG)

    summary.add_result("TOOL", f"{num_appended:n} mains appended to ART.")
    summary.post()


def post_execute(parameters: list[arcpy.Parameter]) -> None:
    """
    Note:
        Unimplemented for this tool.
    """
    pass


def parameters() -> list[arcpy.Parameter]:
    """
    Return the parameters for Append to ART.

    Returns:
        list[arcpy.Parameter]: The list of parameters.
    """
    last_editor = arcpy.Parameter(
        displayName="Editor name",
        name="last_editor",
        datatype="GPString",
        parameterType="Required",
        direction="Input",
    )
    last_editor.value = getpass.getuser().upper()

    on_after_date = arcpy.Parameter(
        displayName="On or after date",
        name="on_after_date",
        datatype="GPDate",
        parameterType="Required",
        direction="Input",
    )
    on_after_date.value = datetime.now() - timedelta(weeks=1)

    water_main_layer = arcpy.Parameter(
        displayName="Water Main Layer",
        name="wm_lyr",
        datatype="GPFeatureLayer",
        parameterType="Required",
        direction="Input",
    )

    art_table = arcpy.Parameter(
        displayName="Asset Reference Drawing Table",
        name="art_table",
        datatype="GPTableView",
        parameterType="Required",
        direction="Input",
    )

    return [last_editor, on_after_date, water_main_layer, art_table]


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

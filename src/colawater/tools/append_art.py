"""
Contains the functions used by the Append to ART tool 
tool and other helper functions.
"""

from datetime import datetime, timedelta
from getpass import getuser
from typing import Optional

import arcpy

import colawater.layer as ly
import colawater.scan as scan
import colawater.status.logging as log
import colawater.status.progressor as pg
import colawater.status.summary as sy
from colawater import attribute as attr
from colawater.error import fallible


def execute(parameters: list[arcpy.Parameter]) -> None:
    """
    Entry point for Append to ART.

    Appends recent integrated and well-sourced mains from a given editor to the
    Asset Reference Table.
    """
    pg.set_progressor("default", "Appending mains to ART...")

    last_editor = parameters[0].valueAsText
    on_after_date = parameters[1].valueAsText
    wm_layer = parameters[2]
    art_table = parameters[3]
    where_water = f"""INTEGRATIONSTATUS = 'Y'
AND LASTEDITOR = '{last_editor}'
AND LASTUPDATE >= '{on_after_date}'
AND LIFECYCLESTATUS = 'Active'
AND OWNEDBY = 1
AND (DATASOURCE = 'SURVGPS' OR DATASOURCE = 'ASB')
"""

    log.info(
        f"Appending mains from [{wm_layer.valueAsText}] to [{art_table.valueAsText}]..."
    )

    mains_appended = _append_to_art(wm_layer.value, where_water, art_table.value)

    sy.add_result(
        wm_layer.valueAsText,
        "Water Mains appended to ART (facility identifier, install date, data source, comments)",
    )
    if mains_appended:
        sy.add_note(wm_layer.valueAsText, attr.CSV_PROCESSING_MSG)
    sy.add_items(mains_appended, csv=True)
    sy.add_result("TOOL", f"{len(mains_appended):n} mains appended to ART.")
    sy.post()


def parameters() -> list[arcpy.Parameter]:
    """
    Returns the parameters for Append to ART.

    Parameters are of type GPString, GPDate, GPFeatureLayer, and GPTableView.

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
    last_editor.value = getuser().upper()

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


@fallible
def _append_to_art(
    wm_lyr: arcpy._mp.Layer,  # pyright: ignore [reportGeneralTypeIssues]
    wm_where_clause: str,
    art_table: arcpy._mp.Layer,  # pyright: ignore [reportGeneralTypeIssues]
) -> list[tuple[Optional[str], ...]]:
    """
    Appends recent integrated and well-sourced mains from a given editor to the
    Asset Reference Table.

    Raises:
        ExecuteError: An error ocurred in the tool execution.

    Returns:
        list[tuple[Optional[str], ...]]: The appended mains.
    """
    mains_appended = []

    with arcpy.da.Editor(  # pyright: ignore [reportGeneralTypeIssues]
        ly.get_workspace(wm_lyr)
    ):
        with arcpy.da.SearchCursor(  # pyright: ignore [reportGeneralTypeIssues]
            ly.get_path(wm_lyr),
            ("FACILITYID", "INSTALLDATE", "DATASOURCE", "COMMENTS"),
            wm_where_clause,
        ) as wm_search_cursor, arcpy.da.InsertCursor(  # pyright: ignore [reportGeneralTypeIssues]
            ly.get_path(art_table),
            (
                "FILELOCATIONCITY",
                "DRAWINGTYPE",
                "DRAWINGDATE",
                "ASSETFACILITYID",
                "ASSETTYPE",
                "SCANNAME",
                "FILELOCATIONCW2020",
            ),
        ) as art_insert_cursor:
            for wm_row in wm_search_cursor:
                fid, install_date, datasource, comments = wm_row
                asset_type = "WAM"
                cw2020_file = None
                city_file = None
                if comments is not None:
                    cw2020_file = str(scan.CW2020_DIR / comments)
                    city_file = str(scan.CITY_DIR / comments)

                art_row = [
                    city_file,
                    datasource,
                    install_date,
                    fid,
                    asset_type,
                    comments,
                    cw2020_file,
                ]
                art_insert_cursor.insertRow(art_row)
                mains_appended.append(wm_row)

    return mains_appended

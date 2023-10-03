"""
Contains the functions used by the Append to ART tool 
tool and other helper functions.
"""

from datetime import datetime, timedelta
from getpass import getuser
from typing import Optional

import arcpy

import colawater.lib.attribute as attr
import colawater.lib.layer as ly
import colawater.lib.scan as scan
import colawater.lib.summary as sy
from colawater.lib.error import fallible
from colawater.lib.progressor import progressor


@progressor("Appending mains to ART...")
def execute(parameters: list[arcpy.Parameter]) -> None:
    """
    Entry point for Append to ART.

    Appends recent integrated and well-sourced mains from a given editor to the Asset Reference Table.

    Arguments:
        parameters (list[arcpy.Parameter]): The list of parameters.
    """
    last_editor = parameters[0].valueAsText
    on_after_date = parameters[1].valueAsText
    wm_layer = parameters[2]
    art_table = parameters[3]
    ignore_nulls = parameters[4]
    where_water = f"""INTEGRATIONSTATUS = 'Y' 
And LASTEDITOR = '{last_editor}' 
And LASTUPDATE >= '{on_after_date}' 
And LIFECYCLESTATUS = 'Active' 
And OWNEDBY = 1 
And (DATASOURCE = 'SURVGPS' Or DATASOURCE = 'ASB')"""

    mains_appended = append_to_art(
        wm_layer.value,
        where_water,
        art_table.value,
        ignore_nulls,
    )

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

    Parameters are of type GPString, GPDate, GPFeatureLayer, GPTableView, and GPBoolean.

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
    now = datetime.now()
    # previous sunday
    on_after_date.value = now - timedelta(days=now.weekday() + 1)

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

    ignore_nulls = arcpy.Parameter(
        displayName="Ignore null values on mains",
        name="ignore_nulls",
        datatype="GPBoolean",
        parameterType="Optional",
        direction="Input",
    )

    return [
        last_editor,
        on_after_date,
        water_main_layer,
        art_table,
        ignore_nulls,
    ]


@fallible
def append_to_art(
    wm_lyr: arcpy._mp.Layer,  # pyright: ignore [reportGeneralTypeIssues]
    wm_where_clause: str,
    art_table: arcpy._mp.Table,  # pyright: ignore [reportGeneralTypeIssues]
    ignore_nulls: bool,
) -> list[tuple[Optional[str], ...]]:
    """
    Appends recent integrated and well-sourced mains from a given editor to the
    Asset Reference Table.

    Arguments:
        wm_lyr (arcpy._mp.Layer): A water main layer from which mains will be read.
        wm_where_clause (str): A SQL where clause used to select a subset of wm_lyr.
        art_table (arcpy._mp.Table): The asset reference table.
        ignore_nulls (bool): Whether to filter rows with None values. If false, ValueError will be raised if a row has a None value.

    Returns:
        list[tuple[Optional[str], ...]]: A list of records of appended mains.

    Raises:
        ExecuteError: An error ocurred in the tool execution.

    Note:
        Modifies input table.
    """
    selected_mains = (
        tuple(i)
        for i in arcpy.da.SearchCursor(  # pyright: ignore [reportGeneralTypeIssues]
            ly.path(wm_lyr),
            ("FACILITYID", "INSTALLDATE", "DATASOURCE", "COMMENTS"),
            wm_where_clause,
        )
    )

    if ignore_nulls:
        selected_mains = (row for row in selected_mains if all(row))
    else:
        for row in selected_mains:
            if not all(row):
                raise ValueError(f"Null attributes on main '{row[0]}'.")

    with arcpy.da.Editor(  # pyright: ignore [reportGeneralTypeIssues]
        ly.workspace(wm_lyr)
    ), arcpy.da.InsertCursor(  # pyright: ignore [reportGeneralTypeIssues]
        ly.path(art_table),
        (
            "FILELOCATIONCITY",
            "DRAWINGTYPE",
            "DRAWINGDATE",
            "ASSETFACILITYID",
            "ASSETTYPE",
            "SCANNAME",
            "FILELOCATIONCW2020",
        ),
    ) as cursor:
        for fid, install_date, datasource, comments in selected_mains:
            cursor.insertRow(
                (
                    str(scan.CITY_DIR / comments) if comments is not None else None,
                    datasource,
                    install_date,
                    fid,
                    "WAM",  # Coded domain value for "Water Main"
                    comments,
                    str(scan.CW2020_DIR / comments) if comments is not None else None,
                )
            )

    return list(selected_mains)

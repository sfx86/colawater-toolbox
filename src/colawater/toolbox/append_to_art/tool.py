"""
Contains the functions used by the Append to ART tool 
tool and other helper functions.
"""

from datetime import datetime, timedelta
from getpass import getuser
from typing import Any

import arcpy

import colawater.lib.scan as scan
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
    editor_name = parameters[0].valueAsText
    on_after_date = parameters[1].valueAsText
    wm_layer = parameters[2].value
    art_table = parameters[3].value

    append_to_art(
        wm_layer,
        art_table,
        editor_name,
        on_after_date,
    )


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

    return [
        last_editor,
        on_after_date,
        water_main_layer,
        art_table,
    ]


@fallible
def append_to_art(
    wm_lyr: arcpy._mp.Layer,  # pyright: ignore [reportGeneralTypeIssues]
    art_table: arcpy._mp.Table,  # pyright: ignore [reportGeneralTypeIssues]
    editor_name: str,
    on_after_date: str,
) -> None:
    """
    Appends recent integrated and well-sourced mains from a given editor to the
    Asset Reference Table.

    Arguments:
        wm_lyr (arcpy._mp.Layer): A water main layer from which mains will be read.
        art_table (arcpy._mp.Table): The asset reference table.
        editor_name (str): The editor whose edits will be used.
        on_after_date (str): The date on or after from which edits will be used.

    Raises:
        ExecuteError: An error ocurred in the tool execution.

    Note:
        Modifies input table.
    """

    def _mk_field_map(fc: Any, input: str, output: str) -> arcpy.FieldMap:
        map = arcpy.FieldMap()
        map.addInputField(fc, input)
        # this makes no sense, but this api is terrible and
        # this is how the docs do it, so whatever
        output_fld = map.outputField
        output_fld.name = output
        map.outputField = output_fld

        return map

    field_mappings = arcpy.FieldMappings()
    for map in (
        _mk_field_map(wm_lyr, input, output)
        for input, output in zip(
            ("FACILITYID", "INSTALLDATE", "DATASOURCE", "COMMENTS"),
            ("ASSETFACILITYID", "DRAWINGDATE", "DRAWINGTYPE", "SCANNAME"),
        )
    ):
        field_mappings.addFieldMap(map)

    arcpy.management.Append(  # pyright: ignore [reportGeneralTypeIssues]
        wm_lyr,
        art_table,
        "NO_TEST",
        field_mappings,
        f"""INTEGRATIONSTATUS = 'Y' 
And LASTEDITOR = '{editor_name}' 
And LASTUPDATE >= '{on_after_date}' 
And LIFECYCLESTATUS = 'Active' 
And OWNEDBY = 1 
And (DATASOURCE = 'SURVGPS' Or DATASOURCE = 'ASB')""",
    )

    # generate this
    where_uncalculated = ""
    arcpy.management.CalculateFields(  # pyright: ignore [reportGeneralTypeIssues]
        art_table,
        fields=(
            (
                "ASSETTYPE",
                "WAM",
            ),
            ("FILELOCATIONCITY", f"'{scan.CITY_DIR}' + !SCANNAME!"),
            (
                "FILELOCATIONCW2020",
                f"'{scan.CW2020_DIR}' + !SCANNAME!",
            ),
        ),
        enforce_domains="ENFORCE_DOMAINS",
    )

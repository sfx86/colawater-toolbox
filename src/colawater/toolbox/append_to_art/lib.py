from typing import Any

import arcpy

from colawater.lib import scan
from colawater.lib.error import fallible


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

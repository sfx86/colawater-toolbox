"""
Contains the functions used by the Append to ART tool 
tool and other helper functions.
"""

from datetime import datetime, timedelta
from getpass import getuser

import arcpy

from colawater.lib import tool
from colawater.toolbox.append_to_art import lib


class AppendToART:
    category = tool.Category.CheckIn.value
    label = "Append to ART"
    description = "Appends new integrated mains to the Asset Reference Table."
    canRunInBackground = False

    def execute(self, parameters: list[arcpy.Parameter]) -> None:
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

        lib.append_to_art(
            wm_layer,
            art_table,
            editor_name,
            on_after_date,
        )

    def getParameterInfo(self) -> list[arcpy.Parameter]:
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

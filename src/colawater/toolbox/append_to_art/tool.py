"""
Contains the functions used by the Append to ART tool 
tool and other helper functions.
"""

from datetime import datetime, timedelta
from getpass import getuser
from typing import Any

import arcpy

from colawater.lib import tool
from colawater.toolbox.append_to_art import lib


class AppendToART:
    category = tool.Category.CheckIn.value
    label = "Append to ART"
    description = "Appends new integrated mains to the Asset Reference Table."
    canRunInBackground = False

    def execute(self, parameters: list[arcpy.Parameter]) -> None:
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

    # fmt: off
    def isLicensed(self) -> bool: return True
    def postExecute(self, parameters: list[arcpy.Parameter]) -> None: return None
    def updateMessages(self, parameters: list[Any]) -> None: return None
    def updateParameters(self, parameters: list[arcpy.Parameter]) -> None: return None
    # fmt: on

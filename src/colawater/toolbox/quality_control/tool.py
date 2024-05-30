"""
Contains the functions used by the Water Quality Control tool 
tool and other helper functions.
"""

import re
from collections.abc import Sequence
from typing import Optional

import arcpy

import colawater.lib.attribute as attr
from colawater.lib import tool

from .lib import fids, mains

_LAYER_START = 4


class QualityControl:
    def execute(self, parameters: list[arcpy.Parameter]) -> None:
        """
        Entry point for Water Quality Control.

        Arguments:
            parameters (list[arcpy.Parameter]): The list of parameters.
        """

        is_checks = parameters[:_LAYER_START]
        layers = parameters[_LAYER_START:]
        wm_layer = layers[-1]
        is_fid_format_check = is_checks[0].value
        is_fid_duplicate_check = is_checks[1].value
        is_wm_file_check = is_checks[2].value
        is_wm_ds_check = is_checks[3].value

        if is_fid_format_check or is_fid_duplicate_check:
            for l in (l for l in layers if not l.value):
                arcpy.AddWarning(f"Layer omitted: {l.displayName}")

        if is_fid_format_check:
            regexes = (
                r"^\d+CA$",
                r"^\d+CV$",
                r"^\d+FT$",
                r"^\d+HYD$",
                r"^\d+SERV$",
                r"^\d+STR$",
                r"^\d+SV$",
                r"^000015-WATER-000\d+$",
            )

            for l, r in ((l, r) for l, r in zip(layers, regexes) if l.value):
                inc_fids = fids.find_faulty(l, re.compile(r))
                # TODO: output as fc

        if is_fid_duplicate_check:
            for l in (l for l in layers if l.value):
                duplicate_fids = fids.find_duplicate(l.value)
                # TODO: output as fc

        if (is_wm_file_check or is_wm_ds_check) and not wm_layer.value:
            arcpy.AddWarning(
                f"Layer omitted: {wm_layer.displayName}, skipping water main checks."
            )
            return

        if is_wm_file_check:
            nonexistent_files = mains.find_faulty_scans(wm_layer)
            # TODO: output as fc

        if is_wm_ds_check:
            inc_datasources = mains.find_unknown_datasources(wm_layer)
            # TODO: output as fc

    def getParameterInfo(self) -> list[arcpy.Parameter]:
        """
        Returns the parameters for Water Quality Control.

        Parameters are 3 of type GPBoolean and 7 of type GPFeatureLayer.

        Returns:
            list[arcpy.Parameter]: The list of parameters.
        """
        checks = [
            arcpy.Parameter(
                displayName=name,
                name=abbrev,
                datatype="GPBoolean",
                parameterType="Optional",
                direction="Input",
            )
            for abbrev, name in (
                # make sure to increment LAYER_START if adding a check here
                ("fid_check", "Check facility identifier format"),
                ("fid_duplicate_check", "Check for duplicate facility identifiers"),
                ("wm_file_check", "Check water main files"),
                ("wm_datasource_check", "Check water main data sources"),
            )
        ]

        lyrs = [
            arcpy.Parameter(
                displayName=name,
                name=abbrev,
                datatype="GPFeatureLayer",
                parameterType="Optional",
                direction="Input",
            )
            for abbrev, name in (
                ("ca_lyr", "Casing"),
                ("cv_lyr", "Control Valve"),
                ("ft_lyr", "Fitting"),
                ("hy_lyr", "Hydrant"),
                ("sl_lyr", "Service Line"),
                ("st_lyr", "Structure"),
                ("sv_lyr", "System Valve"),
                ("wm_lyr", "Water Main"),
            )
        ]

        return [*checks, *lyrs]

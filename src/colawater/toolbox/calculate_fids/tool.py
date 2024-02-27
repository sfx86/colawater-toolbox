"""
Contains the functions used by the Calculate Facility Identifiers
tool and other helper functions.
"""

from getpass import getuser
from typing import Optional

import arcpy

import colawater.lib.layer as ly
from colawater.lib import tool
from colawater.toolbox.calculate_fids import lib


class CalculateFacIDs:
    _category = tool.Category.CheckIn
    category = _category.value
    label = tool.label("Calculate Facility Identifiers", _category)
    canRunInBackground = False

    @tool.entry("Calculating facility identifiers...")
    def execute(self, parameters: list[arcpy.Parameter]) -> None:
        """
        Entry point for Calculate Facility Identifiers.

        Calculates the new facility identifiers for features with given
        placeholder initials starting from a given start value.

        Arguments:
            parameters (list[arcpy.Parameter]): The list of parameters.
        """

        initials = parameters[0].value
        interval = parameters[1].value
        layers = parameters[2].values
        starts = parameters[3:]

        for layer in layers:
            canonical_name = ly.name(layer)
            layer_kind = ly.LayerKind.from_str(canonical_name)

            if layer_kind is None:
                arcpy.AddWarning(f"Unexpected layer name: skipping [{canonical_name}]")
                continue

            start = starts[layer_kind.value.index].value

            if start is None:
                arcpy.AddWarning(f"Start value omitted: skipping [{canonical_name}]")
                continue

            calculate_fid_index = ly.has_field(layer, "FACILITYIDINDEX")
            affix_template = layer_kind.value.affix_template
            new_fid = lib.calculate_fids(
                layer,
                start,
                interval,
                initials,
                affix_template,
                calculate_fid_index,
            )

            if new_fid is not None:
                formatted_fid = affix_template.format(new_fid)
                msg_str = f"{canonical_name}: '{formatted_fid}' -> {new_fid}"
            else:
                msg_str = f"{canonical_name}: None used"

            sy.add_item(msg_str)

        sy.post()

    def getParameterInfo(self) -> list[arcpy.Parameter]:
        """
        Returns the parameters for Calculate Facility Identifiers.

        Parameters are of type GPString, GPLong, GPFeatureLayer multivalue, and 7 GPLong.

        Returns:
            list[arcpy.Parameter]: The list of parameters.
        """
        initials = arcpy.Parameter(
            displayName="Initials",
            name="initials",
            datatype="GPString",
            parameterType="Required",
            direction="Input",
        )
        initials.value = getuser()[:3].upper()

        interval = arcpy.Parameter(
            displayName="Global Interval",
            name="interval",
            datatype="GPLong",
            parameterType="Required",
            direction="Input",
        )
        interval.value = 2

        layers = arcpy.Parameter(
            displayName="Water Layers",
            name="layers",
            datatype="GPFeatureLayer",
            parameterType="Required",
            direction="Input",
            multiValue=True,
        )

        starts = (
            arcpy.Parameter(
                displayName=f"Start Value: {name}",
                name=f"{abbrev}_start",
                datatype="GPLong",
                parameterType="Optional",
                direction="Input",
            )
            for abbrev, name in (
                ("ca", "Casing"),
                ("cv", "Control Valve"),
                ("ft", "Fitting"),
                ("hy", "Hydrant"),
                ("sl", "Service Line"),
                ("st", "Structure"),
                ("sv", "System Valve"),
                ("wm", "Water Main"),
            )
        )

        return [initials, interval, layers, *starts]

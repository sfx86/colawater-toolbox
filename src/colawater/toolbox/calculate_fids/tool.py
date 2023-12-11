"""
Contains the functions used by the Calculate Facility Identifiers
tool and other helper functions.
"""

from getpass import getuser
from typing import Optional

import arcpy

import colawater.lib.layer as ly
import colawater.lib.summary as sy
from colawater.lib.error import fallible
from colawater.lib.layer import LayerKind
from colawater.lib.progressor import progressor


@progressor("Calculating facility identifiers...")
def execute(parameters: list[arcpy.Parameter]) -> None:
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

    sy.add_result("TOOL", "New start values:")

    for layer in layers:
        canonical_name = ly.name(layer)
        layer_kind = ly.kind(layer)

        if layer_kind is None:
            arcpy.AddWarning(f"Unexpected layer name: skipping [{canonical_name}]")
            continue

        start = starts[layer_kind.value.index].value

        if start is None:
            arcpy.AddWarning(f"Start value omitted: skipping [{canonical_name}]")
            continue

        calculate_fid_index = (
            True
            if layer_kind
            in {
                LayerKind.Casing,
                LayerKind.ControlValve,
                LayerKind.Fitting,
                LayerKind.Hydrant,
                LayerKind.WaterMain,
            }
            else False
        )

        affix_template = layer_kind.value.affix_template
        new_fid = calculate_fids(
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


def parameters() -> list[arcpy.Parameter]:
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


@fallible
def calculate_fids(
    layer: arcpy._mp.Layer,  # pyright: ignore [reportGeneralTypeIssues]
    start: int,
    interval: int,
    initials: str,
    affix_template: str,
    calculate_fid_index: bool,
) -> Optional[int]:
    """
    Calculates the facility identifiers for the provided layer.

    Also updates the substituted initials with the new facility identifiers
    in the provided layer.

    Arguments:
        layer (arcpy._mp.Layer): The layer value.
        start (int): The start value.
        interval (int): The interval to increment the facility identifier.
        initials (str): The initials to replace with the calculated facility identifiers.
        affix_template (str): A format string with one anonymous brace pair.
        calculate_fid_index (bool): Whether to calculate the FID indices for ``layer``.

    Returns:
        Optional[int]: The final facility identifier value, plus one interval to be used
             as an input for the next tool execution, or None if no values
             matching ``initials`` were found.

    Raises:
        ExecuteError: An error ocurred in the tool execution.

    Note:
        Modifies input layer.
    """
    final = start
    path = ly.path(layer)

    with arcpy.da.Editor(  # pyright: ignore [reportGeneralTypeIssues]
        ly.workspace(layer)
    ):
        # only these layers have FACILITYIDINDEX
        if calculate_fid_index:
            with arcpy.da.UpdateCursor(  # pyright: ignore [reportGeneralTypeIssues]
                path, ("FACILITYID", "FACILITYIDINDEX"), f"FACILITYID = '{initials}'"
            ) as cursor:
                for _ in cursor:
                    cursor.updateRow((affix_template.format(final), final))
                    final += interval
        else:
            with arcpy.da.UpdateCursor(  # pyright: ignore [reportGeneralTypeIssues]
                path, ("FACILITYID"), f"FACILITYID = '{initials}'"
            ) as cursor:
                for _ in cursor:
                    cursor.updateRow((affix_template.format(final),))
                    final += interval

    if final == start:
        return None

    return final

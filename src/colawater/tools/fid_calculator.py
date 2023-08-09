"""
Contains the functions used by the Calculate Facility Identifiers
tool and other helper functions.
"""

from getpass import getuser

import arcpy

import colawater.layer as ly
import colawater.status.logging as log
import colawater.status.progressor as pg
import colawater.status.summary as sy
from colawater.error import fallible

_LAYER_START = 2


def execute(parameters: list[arcpy.Parameter]) -> None:
    """
    Entry point for Calculate Facility Identifiers.

    Calculates the new facility identifiers for features with given
    placeholder initials starting from a given start value.

    Raises:
        ExecuteError: An error ocurred in the tool execution.
    """
    pg.set_progressor("step", "Calculating facility identifiers...", 0, 6)

    initials = parameters[0].value
    interval = parameters[1].value

    # first two parameters are not needed for the tight loop
    items = zip(
        (p for p in parameters[_LAYER_START:] if p.name.endswith("_lyr")),
        (p for p in parameters[_LAYER_START:] if p.name.endswith("_start")),
    )

    sy.add_result("TOOL", "New start values:")

    for layer, start in items:
        if not (layer.value and start.value):
            log.warning(f"Layer or start value omitted: skipping [{layer.displayName}]")
            pg.increment()
            continue

        log.info(f"Calculating facility identifiers for [{layer.valueAsText}]...")

        new_fid = _calc_fids(layer, start, interval, initials)

        sy.add_item(f"{layer.displayName}: {new_fid}")
        log.info(f"[{layer.valueAsText}] finished.")
        pg.increment()

    sy.post()


def parameters() -> list[arcpy.Parameter]:
    """
    Returns the parameters for Calculate Facility Identifiers.

    Parameters are of type GPString, GPLong, and 7 pairs of GPFeatureLayer and GPLong.

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

    templates = (
        ("ca_lyr", "Casing"),
        ("cv_lyr", "Control Valve"),
        ("ft_lyr", "Fitting"),
        ("hy_lyr", "Hydrant"),
        ("sl_lyr", "Service Line"),
        ("st_lyr", "Structure"),
        ("sv_lyr", "System Valve"),
        ("wm_lyr", "Water Main"),
    )

    input_layers = [
        f(abbrev, name)
        for abbrev, name in templates
        for f in (
            lambda abbrev, name: arcpy.Parameter(
                displayName=name,
                name=abbrev,
                datatype="GPFeatureLayer",
                parameterType="Optional",
                direction="Input",
            ),
            lambda abbrev, name: arcpy.Parameter(
                displayName=f"{name} Start Value",
                name=f"{abbrev}_start",
                datatype="GPLong",
                parameterType="Optional",
                direction="Input",
            ),
        )
    ]

    return [initials, interval, *input_layers]


def update_parameters(parameters: list[arcpy.Parameter]) -> None:
    """
    Enables layer start values if their associated layer is set and ensures start values are greater than zero.

    Arguments:
        parameters (list[arcpy.Parameter]): The list of parameters.
    """
    for l, s in zip(
        (p for p in parameters[_LAYER_START:] if p.name.endswith("_lyr")),
        (p for p in parameters[_LAYER_START:] if p.name.endswith("_start")),
    ):
        s.enabled = True if l.value else False
        # short circuiting prevents NoneType and Int comparision
        s.value = 1 if s.value is not None and s.value < 1 else s.value


@fallible
def _calc_fids(
    layer: arcpy.Parameter,
    start: arcpy.Parameter,
    interval: int,
    initials: str,
) -> str:
    """
    Calculates the facility identifiers for the provided layer.

    Also updates the substituted initials with the new facility identifiers
    in the provided layer.

    Arguments:
        layer (arcpy.Parameter): The layer parameter.
        start (arpcy.Parameter): The start value parameter.
        interval (int): The interval to increment the facility identifier.
        initials (str): The initials to replace with the calculated facility identifiers.

    Returns:
        str: The final facility identifier plus one interval to be used
             as an input for the next tool execution.

    Raises:
        ExecuteError: An error ocurred in the tool execution.
    """

    # map of layer abbreviation to its affixes
    affix_map = {
        "ca_lyr": ("", "CA"),
        "cv_lyr": ("", "CV"),
        "ft_lyr": ("", "FT"),
        "hy_lyr": ("", "HYD"),
        "sl_lyr": ("", "SERV"),
        "st_lyr": ("", "STR"),
        "sv_lyr": ("", "SV"),
        "wm_lyr": ("000015-WATER-000", ""),
    }
    fields = ("FACILITYID", "FACILITYIDINDEX")
    where_initials = f"FACILITYID = '{initials}'"

    incr = start.value
    lyr_path = ly.get_path(layer.value)
    workspace = ly.get_workspace(layer.value)
    prefix, suffix = affix_map[layer.name]

    with arcpy.da.Editor(workspace):  # type: ignore
        # only these layers have FACILITYIDINDEX
        if layer.name in {"ca_lyr", "cv_lyr", "ft_lyr", "hy_lyr", "wm_lyr"}:
            with arcpy.da.UpdateCursor(  # type: ignore
                lyr_path, fields, where_initials
            ) as cursor:
                for _ in cursor:
                    cursor.updateRow((f"{prefix}{incr}{suffix}", incr))
                    incr += interval
        else:
            with arcpy.da.UpdateCursor(  # type: ignore
                lyr_path, fields[0], where_initials
            ) as cursor:
                for _ in cursor:
                    # leave FACILITYIDINDEX alone; logic is otherwise identicial
                    cursor.updateRow((f"{prefix}{incr}{suffix}"))
                    incr += interval

    return f"{prefix}{incr}{suffix}"

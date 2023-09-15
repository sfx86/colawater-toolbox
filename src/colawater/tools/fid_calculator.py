"""
Contains the functions used by the Calculate Facility Identifiers
tool and other helper functions.
"""

import re
from getpass import getuser

import arcpy

import colawater.layer as ly
import colawater.status.logging as log
import colawater.status.progressor as pg
import colawater.status.summary as sy
from colawater.error import fallible


def execute(parameters: list[arcpy.Parameter]) -> None:
    """
    Entry point for Calculate Facility Identifiers.

    Calculates the new facility identifiers for features with given
    placeholder initials starting from a given start value.

    Arguments:
        parameters (list[arcpy.Parameter]): The list of parameters.
    """
    pg.set_progressor("default", "Calculating facility identifiers...")

    initials = parameters[0].value
    interval = parameters[1].value
    layers = parameters[2].values
    starts = parameters[3:]
    layer_names = (
        "waCasing",
        "waControlValve",
        "waFitting",
        "waHydrant",
        "waServiceLine",
        "waStructure",
        "waSystemValve",
        "waWaterMain",
    )
    index_map: dict[str, int] = dict((name, i) for i, name in enumerate(layer_names))
    affix_map: dict[str, str] = dict(
        zip(
            layer_names,
            (
                "{}CA",
                "{}CV",
                "{}FT",
                "{}HYD",
                "{}SERV",
                "{}STR",
                "{}SV",
                "000015-WATER-000{}",
            ),
        )
    )

    sy.add_result("TOOL", "New start values:")

    for layer in layers:
        layer_name = ly.name(layer)
        search_name = re.compile(
            r"(waCasing|waControlValve|waFitting|waHydrant|waServiceLine|waStructure|waSystemValve|waWaterMain)"
        ).search(layer_name)
        match_name = search_name.group(0) if search_name is not None else ""

        try:
            start_idx = index_map[match_name]
        except KeyError:
            log.warning(f"Unexpected layer name: [{layer_name}]")
            continue

        if (start := starts[start_idx].value) is None:
            log.warning(f"Start value omitted: skipping [{layer_name}]")
            continue

        log.info(f"Calculating facility identifiers for [{layer_name}]...")

        affix_template = affix_map[match_name]
        new_fid = calculate_fids(
            layer,
            match_name,
            {
                "waCasing",
                "waControlValve",
                "waFitting",
                "waHydrant",
                "waWaterMain",
            },
            start,
            interval,
            initials,
            affix_template,
        )

        if new_fid != -1:
            formatted_fid = affix_template.format(new_fid)
            sy.add_item(f"{layer_name}: '{formatted_fid}' -> {new_fid}")
        else:
            sy.add_item(f"{layer_name}: None used")

        log.info(f"[{layer_name}] finished.")

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
    match_name: str,
    fid_idx_layers: set[str],
    start: int,
    interval: int,
    initials: str,
    affix_template: str,
) -> int:
    """
    Calculates the facility identifiers for the provided layer.

    Also updates the substituted initials with the new facility identifiers
    in the provided layer.

    Arguments:
        layer (arcpy._mp.Layer): The layer value.
        match_name (str): The layer name to match against ``fid_idx_layers``.
        fid_idx_layers (set[str]): The set of layer names which the facility ID index will be calculated.
        start (int): The start value.
        interval (int): The interval to increment the facility identifier.
        initials (str): The initials to replace with the calculated facility identifiers.
        affix_template (str): A format string with one anonymous brace pair.

    Returns:
        int: The final facility identifier value, plus one interval to be used
             as an input for the next tool execution, or -1 if no values
             matching ``initials`` were found.

    Raises:
        ExecuteError: An error ocurred in the tool execution.

    Note:
        Modifies input layer.
    """
    incr = start
    path = ly.path(layer)

    with arcpy.da.Editor(  # pyright: ignore [reportGeneralTypeIssues]
        ly.workspace(layer)
    ):
        # only these layers have FACILITYIDINDEX
        if match_name in fid_idx_layers:
            with arcpy.da.UpdateCursor(  # pyright: ignore [reportGeneralTypeIssues]
                path, ("FACILITYID", "FACILITYIDINDEX"), f"FACILITYID = '{initials}'"
            ) as cursor:
                for _ in cursor:
                    cursor.updateRow((affix_template.format(incr), incr))
                    incr += interval
        else:
            with arcpy.da.UpdateCursor(  # pyright: ignore [reportGeneralTypeIssues]
                path, ("FACILITYID"), f"FACILITYID = '{initials}'"
            ) as cursor:
                for _ in cursor:
                    # leave FACILITYIDINDEX alone; logic is otherwise identicial
                    cursor.updateRow((affix_template.format(incr),))
                    incr += interval

    if incr == start:
        return -1

    return incr

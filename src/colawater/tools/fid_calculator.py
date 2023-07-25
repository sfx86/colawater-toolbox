"""
Contains the functions used by the Calculate Facility Identifiers
tool and other helper functions.
"""

import arcpy
from colawater.utils.constants import RUNTIME_ERROR_MSG
from colawater.utils.functions import get_layer_path
from colawater.utils.status import StatusUpdater
from colawater.utils.summary import SummaryBuilder


def execute(parameters: list[arcpy.Parameter]) -> None:
    """
    Entry point for Calculate Facility Identifiers.

    Calculates the new facility identifiers for features with given
    placeholder initials starting from a given start value.

    Raises:
        ExecutionError: An error ocurred in the tool execution.
    """
    arcpy.SetProgressor("step", "Calculating facility identifiers...", 0, 13)
    status = StatusUpdater()
    summary = SummaryBuilder()
    summary.add_header("New start values:")

    _calc_fids(parameters, status, summary)

    summary.post()


def post_execute(parameters: list[arcpy.Parameter]) -> None:
    """
    Note:
        Unimplemented for this tool.
    """
    pass


def parameters() -> list[arcpy.Parameter]:
    """
    Return the parameters for Calculate Facility Identifiers.

    Returns:
        list[arcpy.Parameter]: The list of parameters.
    """
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
    # layer param list
    input_layers: list[arcpy.Parameter] = []
    for abbrev, name in templates:
        input_layers.extend(_water_param_pair(abbrev, name))
    # facility identifier placeholder initials
    initials = arcpy.Parameter(
        displayName="Initials",
        name="initials",
        datatype="GPString",
        parameterType="Required",
        direction="Input",
    )
    # interval to increment the start each loop
    interval = arcpy.Parameter(
        displayName="Global Interval",
        name="interval",
        datatype="GPLong",
        parameterType="Required",
        direction="Input",
    )
    interval.value = 2

    return [initials, interval, *input_layers]


def update_parameters(parameters: list[arcpy.Parameter]) -> None:
    """
    Update parameters to ensure their correctness.

    Enables layer start values if their associated layer is set and
    ensures start values are greater than zero.

    Arguments:
        parameters (list[arcpy.Parameter]): The list of parameters.
    """
    for i, p in enumerate(parameters):
        lyr = p.value
        lyr_abbrev = p.name
        if lyr_abbrev.endswith("_lyr"):
            # showing or hiding the start value if the layer is set or not
            start = parameters[i + 1]
            start.enabled = True if lyr else False
        elif lyr_abbrev.endswith("_start"):
            # short circuiting prevents NoneType and Int comparision
            p.value = 1 if p.value and p.value < 1 else p.value


def update_messages(parameters: list[arcpy.Parameter]) -> None:
    """
    Note:
        Unimplemented for this tool.
    """
    pass


def _calc_fids(
    parameters: list[arcpy.Parameter],
    status: StatusUpdater,
    summary: SummaryBuilder,
) -> None:
    """
    Calculates the facility identifiers for the layers in the parameter list.

    Arguments:
        parameters (list[arcpy.Parameter]): The list of parameters for this tool.
        status (StatusUpdater): The status for this tool.
        summary (SummaryBuilder): The summary for this tool.

    Raises:
        ExecutionError: An error ocurred in the tool execution.
    """
    initials = parameters[0].value
    interval = parameters[1].value

    # first two parameters are not needed for the tight loop
    p_iter = iter(parameters[2:])

    for p in p_iter:
        lyr = p.value
        # associated start value is always next
        # using next inside of a for loop is sketchy, but given that the parameter
        # list is of a known shape, domain knowledge allows for this pattern
        #
        # it also prevents the need to filter() the list or have some if condition,
        # which is cool
        start = next(p_iter).value

        # guard against None
        if not (lyr and start):
            status.update_warn(
                f"Layer or start value omitted: skipping [{p.displayName}]"
            )
            # non-warn runs increment the progressor twice
            status.increment_progressor()
            continue

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
        incr = start
        lyr_abbrev = p.name
        lyr_name = p.displayName
        lyr_name_long = p.valueAsText
        lyr_path = get_layer_path(lyr)
        prefix, suffix = affix_map[lyr_abbrev]
        where_initials = f"FACILITYID = '{initials}'"

        status.update_info(f"Calculating facility identifiers for [{lyr_name_long}]...")

        try:
            # only these layers have FACILITYIDINDEX
            if lyr_abbrev in (
                "ca_lyr",
                "cv_lyr",
                "ft_lyr",
                "hy_lyr",
                "wm_lyr",
            ):
                with arcpy.da.UpdateCursor(lyr_path, fields, where_initials) as cursor:
                    for row in cursor:
                        # update fid and fid index with incr value
                        row[0] = f"{prefix}{incr}{suffix}"
                        row[1] = incr
                        cursor.updateRow(row)
                        incr += interval
            else:
                with arcpy.da.UpdateCursor(
                    lyr_path, fields[0], where_initials
                ) as cursor:
                    for row in cursor:
                        # leave FACILITYIDINDEX alone; logic is otherwise identicial
                        row[0] = f"{prefix}{incr}{suffix}"
                        cursor.updateRow(row)
                        incr += interval
        # arcpy should only ever throw RuntimeError here, but you never know
        except Exception:
            # post existing summaries as to not lose information
            summary.post()
            status.update_err(RUNTIME_ERROR_MSG)

        status.update_info(f"[{lyr_name_long}] finished.")
        new_fid = f"{prefix}{incr}{suffix}"
        summary.add_item(f"{lyr_name}: {new_fid}")


def _water_param_pair(
    abbrev: str, name: str
) -> tuple[arcpy.Parameter, arcpy.Parameter]:
    """
    Returns a tuple of a layer parameter and start value parameter.

    Arguments:
        abbrev (str): The new layer's abbreviated name.
        name (str): The new layer's display name.

    Returns:
        tuple[arcpy.Parameter, arcpy.Parameter]: The parameter pair.
    """
    return (
        # layer portion
        arcpy.Parameter(
            displayName=name,
            name=abbrev,
            datatype="GPFeatureLayer",
            parameterType="Optional",
            direction="Input",
        ),
        # start value portion
        arcpy.Parameter(
            displayName=f"{name} Start Value",
            name=f"{abbrev}_start",
            datatype="GPLong",
            parameterType="Optional",
            direction="Input",
        ),
    )

import arcpy
import utils
from dataclasses import dataclass


def execute(parameters: list[arcpy.Parameter]) -> None:
    """Entry point."""
    arcpy.SetProgressor("step", "Calculating facility identifiers...", 0, 13)
    status = utils.StatusUpdater()
    summary = utils.SummaryBuilder()
    summary.add_header("New start values:")

    initials = parameters[0].value
    interval = parameters[1].value

    for i, p in enumerate(parameters):
        if p.name.endswith("_lyr"):
            layer = p.value
            layer_name = p.valueAsText
            layer_short_name = p.name
            layer_disp_name = p.displayName
            start = parameters[i + 1].value
            # see the function docstrings for info on the rest of the execution
            if layer and start:
                status.update_info(
                    f"Calculating facility identifiers for '{layer_name}'..."
                )
                # side effect of calculating the fids but returns the exclusive end of the range
                # [start, end)
                new_fid = _calc_fids(
                    layer, layer_short_name, initials, start, interval, status
                )
                status.update_info(f"'{layer_name}' finished.")
                summary.add_item(f"{layer_disp_name}: {new_fid}")
            else:
                status.update_warn(
                    f"Layer or start value omitted: skipping '{p.displayName}'"
                )
                # non-warn runs bump the progressor twice
                status.bump_progressor()
    summary.post()


def post_execute(parameters: list[arcpy.Parameter]) -> None:
    pass


def parameters() -> list[arcpy.Parameter]:
    """Return a list of arcpy.Parameter."""
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
    # water layer param list
    input_layers = []
    for short_name, disp_name in templates:
        input_layers.extend(_water_layer_parameter(short_name, disp_name))
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
    """Update parameters."""
    for i, p in enumerate(parameters):
        layer = p.value
        layer_short_name = p.name
        if layer_short_name.endswith("_lyr"):
            # showing or hiding the start value if the layer is set or not
            start = parameters[i + 1]
            start.enabled = True if layer else False
        elif layer_short_name.endswith("_start"):
            # short circuiting prevents NoneType and Int comparision
            p.value = 1 if p.value and p.value < 1 else p.value


def update_messages(parameters: list[arcpy.Parameter]) -> None:
    pass


@dataclass(frozen=True)
class _LayerKV:
    # layer short name -> prefix, suffix, whether or not fid index is calculated
    ca_lyr = ("", "CA", True)
    cv_lyr = ("", "CV", True)
    ft_lyr = ("", "FT", True)
    hy_lyr = ("", "HYD", True)
    sl_lyr = ("", "SERV", False)
    st_lyr = ("", "STR", False)
    sv_lyr = ("", "SV", False)
    wm_lyr = ("000015-WATER-000", "", True)


def _calc_fids(
    layer: arcpy._mp.Layer,
    layer_short_name: str,
    initials: str,
    start: int,
    interval: int,
    status: utils.StatusUpdater,
) -> str:
    """Return a string with the new facility identifier for a given layer."""
    layer_kv = _LayerKV()
    layer_path = utils.get_layer_path(layer)
    prefix, suffix, id_flag = getattr(layer_kv, layer_short_name)
    increment = start

    try:
        # https://pro.arcgis.com/en/pro-app/latest/arcpy/data-access/updatecursor-class.htm
        if id_flag:
            with arcpy.da.UpdateCursor(
                layer_path,
                ("FACILITYID", "FACILITYIDINDEX"),
                where_clause=f"FACILITYID = '{initials}'",
            ) as cursor:
                for row in cursor:
                    row[0] = f"{prefix}{increment}{suffix}"
                    row[1] = increment
                    increment += interval
                    cursor.updateRow(row)
        else:
            with arcpy.da.UpdateCursor(
                layer_path, "FACILITYID", where_clause=f"FACILITYID = '{initials}'"
            ) as cursor:
                for row in cursor:
                    row[0] = f"{prefix}{increment}{suffix}"
                    increment += interval
                    cursor.updateRow(row)
    except RuntimeError:
        # arcgis needs to have exclusive write access to the layer's database,
        # so it complains about not being able to acquire the lock if you have the lock with the attribute table
        status.update_err(
            "If you see an error that says 'RuntimeError: Cannot acquire a lock.', close the attribute tables of the layers for which you are trying to calculate facility identifiers. If that still does not work, go find whomever wrote this tool and ask them about it."
        )

    return f"{prefix}{increment}{suffix}"


def _water_layer_parameter(
    short_name: str, disp_name: str
) -> tuple[arcpy.Parameter, arcpy.Parameter]:
    """Return a tuple of a water layer parameter and facility identifier start value parameter."""
    # https://pro.arcgis.com/en/pro-app/latest/arcpy/classes/parameter.htm
    layer = arcpy.Parameter(
        displayName=disp_name,
        name=short_name,
        datatype="GPFeatureLayer",
        parameterType="Optional",
        direction="Input",
    )
    start = arcpy.Parameter(
        displayName=f"{disp_name} Start Value",
        name=f"{short_name}_start",
        datatype="GPLong",
        parameterType="Optional",
        direction="Input",
    )

    return (layer, start)

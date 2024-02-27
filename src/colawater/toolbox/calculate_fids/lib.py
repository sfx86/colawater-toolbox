from typing import Optional

import arcpy

from colawater.lib import layer
from colawater.lib.error import fallible


@fallible
def calculate_fids(
    layer: arcpy._mp.Layer,  # pyright: ignore [reportGeneralTypeIssues]
    start: int,
    interval: int,
    placeholder: str,
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
        placeholder (str): The placeholder to replace with the calculated facility identifiers.
        affix_template (str): A format string with one anonymous brace pair.
        calculate_fid_index (bool): Whether to calculate the FID indices for ``layer``.

    Returns:
        Optional[int]: The final facility identifier value, plus one interval to be used
             as an input for the next tool execution, or None if no values
             matching ``placeholder`` were found.

    Raises:
        ExecuteError: An error ocurred in the tool execution.

    Note:
        Modifies input layer.
    """
    counter = start
    path = layer.path(layer)
    where_facid = f"FACILITYID = '{placeholder}'"
    fields = ("FACILITYID", "FACILITYIDINDEX")

    with arcpy.da.Editor(  # pyright: ignore [reportGeneralTypeIssues]
        layer.workspace(layer)
    ):
        if calculate_fid_index:
            with arcpy.da.UpdateCursor(  # pyright: ignore [reportGeneralTypeIssues]
                path, fields, where_facid
            ) as cursor:
                for _ in cursor:
                    cursor.updateRow((affix_template.format(counter), counter))
                    counter += interval
        else:
            with arcpy.da.UpdateCursor(  # pyright: ignore [reportGeneralTypeIssues]
                path, fields[0], where_facid
            ) as cursor:
                for _ in cursor:
                    cursor.updateRow((affix_template.format(counter),))
                    counter += interval

    if counter == start:
        return None

    return counter

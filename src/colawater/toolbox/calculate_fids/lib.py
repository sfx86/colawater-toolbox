from enum import Enum, unique
from typing import Any, Optional

import arcpy

from colawater.lib import desc
from colawater.lib import layer as ly
from colawater.lib.error import fallible


@unique
class AssetType(Enum):
    """
    Possible asset types.
    """

    Casing = "Casing"
    ControlValve = "Control Valve"
    Fitting = "Fitting"
    Hydrant = "Hydrant"
    ServiceLine = "Service Line"
    Structure = "Structure"
    SystemValve = "System Valve"
    WaterMain = "Water Main"


@unique
class FacIDTemplate(Enum):
    """
    Facility Identifier formats corresponding to the variants of AssetType
    """

    Casing = "{}CA"
    ControlValve = "{}CV"
    Fitting = "{}FT"
    Hydrant = "{}HYD"
    ServiceLine = "{}SERV"
    Structure = "{}STR"
    SystemValve = "{}SV"
    WaterMain = "000015-WATER-000{}"


# every asset type must have an associated template
assert AssetType._member_names_ == FacIDTemplate._member_names_


@fallible
def calculate_fids(
    layer: arcpy._mp.Layer,  # pyright: ignore [reportAttributeAccessIssue]
    asset_type: AssetType,
    placeholder: str,
    interval: int,
    start: int,
) -> int:
    """
    Calculates and updates the facility identifiers for the provided layer.
    If the layer has a facility identifier index, also update that.

    Arguments:
        layer (arcpy._mp.Layer): The layer value.
        asset_type (AssetType): The asset type.
        placeholder (str): The placeholder to replace with the calculated facility identifiers.
        interval (int): The interval to increment the facility identifier.
        start (int): The start value.

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
    facid_template = FacIDTemplate[asset_type.name].value
    fields = ("FACILITYID", "FACILITYIDINDEX")
    workspace = desc.path(layer)
    where_facid = f"{fields[0]} = '{placeholder}'"

    with arcpy.da.Editor(workspace):  # pyright: ignore [reportAttributeAccessIssue]
        if ly.has_field(layer, fields[1]):
            with arcpy.da.UpdateCursor(  # pyright: ignore [reportAttributeAccessIssue]
                layer,
                fields,
                where_facid,
            ) as cursor:
                for _ in cursor:
                    cursor.updateRow((facid_template.format(counter), counter))
                    counter += interval
        else:
            with arcpy.da.UpdateCursor(  # pyright: ignore [reportAttributeAccessIssue]
                layer,
                fields[0],
                where_facid,
            ) as cursor:
                for _ in cursor:
                    cursor.updateRow((facid_template.format(counter),))
                    counter += interval

    return counter

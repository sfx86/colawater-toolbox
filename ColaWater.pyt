# -*- coding: utf-8 -*-

import arcpy
import utils


class Toolbox(object):
    def __init__(self):
        """Define the toolbox (the name of the toolbox is the name of the
        .pyt file)."""
        self.label = "Columbia Water"
        self.alias = "ColaWater"
        self.tools = [CalculateFacilityIdentifiers]


class CalculateFacilityIdentifiers(object):
    """Calculates the various facility identifiers and facility identifier indices for water layers."""

    def __init__(self) -> None:
        """Initialize tool metadata and capabilities."""
        self.label = "Calculate Facility Identifiers"
        self.description = "Calculates the various facility identifiers and facility identifier indices for water layers."
        self.canRunInBackground = False

    def getParameterInfo(self) -> list[arcpy.Parameter]:
        """Return a list of parameters."""

        def water_lyr_param(
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
            input_layers.extend(water_lyr_param(short_name, disp_name))
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

    def updateParameters(self, parameters: list[arcpy.Parameter]) -> None:
        """Modify parameters to keep them valid. Called every time a parameter is updated."""
        for i, p in enumerate(parameters):
            layer = p.value
            layer_short_name = p.name
            if layer_short_name.endswith("_lyr"):
                # showing or hiding the start value if the layer is set or not
                start = parameters[i + 1]
                if not layer:
                    start.enabled = False
                else:
                    start.enabled = True
            elif layer_short_name.endswith("_start"):
                start_value = p.value
                # short circuiting prevents NoneType and Int comparision
                if start_value and start_value < 1:
                    start_value = 1

    def execute(self, parameters, messages) -> None:
        """Tool entry point."""
        initials = parameters[0].value
        interval = parameters[1].value

        arcpy.SetProgressor("step", "Calculating facility identifiers...", 0, 13)
        status = utils.StatusUpdater(messages)
        summary = utils.SummaryBuilder(messages)
        summary.add_header("New start values:")

        for i, p in enumerate(parameters):
            if p.name.endswith("_lyr"):
                layer = p.value
                layer_name = p.valueAsText
                layer_short_name = p.name
                layer_disp_name = p.displayName
                start = parameters[i + 1].value
                # see the function docstrings for info on the rest of the execution
                if layer and start:
                    status.update_info(f"Calculating facility identifiers for '{layer_name}'...")
                    new_fid = self.calc_fids(
                        layer, layer_short_name, initials, start, interval, status
                    )
                    status.update_info(f"'{layer_name}' finished.")
                    summary.add_item(f"{layer_disp_name}: {new_fid}")
                else:
                    status.update_warn(
                        f"Layer or start value omitted: skipping '{p.displayName}'"
                    )
        summary.post()

    def calc_fids(
        self,
        layer,
        layer_short_name: str,
        initials: str,
        start: int,
        interval: int,
        status: utils.StatusUpdater,
    ) -> str:
        """Return a string with the new facility identifier for a given layer."""
        layer_kv = {
            # layer short name -> prefix, suffix, whether or not fid index is calculated
            "ca_lyr": ("", "CA", True),
            "cv_lyr": ("", "CV", True),
            "ft_lyr": ("", "FT", True),
            "hy_lyr": ("", "HYD", True),
            "sl_lyr": ("", "SERV", False),
            "st_lyr": ("", "STR", False),
            "sv_lyr": ("", "SV", False),
            "wm_lyr": ("000015-WATER-000", "", True),
        }

        layer_path = utils.getLayerPath(layer)
        prefix, suffix, id_flag = layer_kv[layer_short_name]
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

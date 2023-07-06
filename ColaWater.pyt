# -*- coding: utf-8 -*-

import arcpy


class Toolbox(object):
    def __init__(self):
        """Define the toolbox (the name of the toolbox is the name of the
        .pyt file)."""
        self.label = "Columbia Water"
        self.alias = "ColaWater"

        # List of tool classes associated with this toolbox
        self.tools = [CalculateFacilityIdentifiers]


class CalculateFacilityIdentifiers(object):
    def __init__(self) -> None:
        """Initialize tool metadata and capabilities."""
        self.label = "Calculate Facility Identifiers"
        self.description = "Calculates the various facility identifiers and facility identifier indices for water layers."
        self.canRunInBackground = False

    def getParameterInfo(self) -> list[arcpy.Parameter]:
        """Return a list of parameter definitions."""

        def water_lyr_param(
            short_name: str, disp_name: str
        ) -> tuple[arcpy.Parameter, arcpy.Parameter]:
            """Return a tuple of a water layer parameter and facility identifier start value parameter
            given a short name and a display name."""
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

        # tuple of tuples of arguments for water_lyr_param
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

        # creating input layers with templates and the water_lyr_param helper function
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
                # prevent number values < 1
                start_value = p.value
                # short circuiting prevents NoneType and Int comparision
                if start_value and start_value < 1:
                    start_value = 1

    def execute(self, parameters, messages) -> None:
        """Tool entry point."""
        # give more readable names to params and also avoid indexing a bunch of times
        initials = parameters[0].value
        interval = parameters[1].value

        # initialize progress bar
        arcpy.SetProgressor("step", "Calculating facility identifiers...", 0, 13)
        # create instance of NewStarts helper class
        new_starts = self.NewStarts()

        for i, p in enumerate(parameters):
            if p.name.endswith("_lyr"):
                # give more readable names to values and also avoid getting attrs or indexing a bunch of times
                layer = p.value
                layer_name = p.valueAsText
                layer_short_name = p.name
                layer_disp_name = p.displayName
                start = parameters[i + 1].value

                # see the function docstrings for info on the rest of the execution
                if layer and start:
                    self.update_info(
                        messages,
                        f"Calculating facility identifiers for '{layer_name}'...",
                    )
                    new_fid = self.calculate_facility_identifiers(
                        layer, layer_short_name, initials, start, interval, messages
                    )
                    self.update_info(messages, f"'{layer_name}' finished.")

                    new_starts.update(layer_short_name, new_fid)
                else:
                    self.update_warn(
                        messages,
                        f"Layer or start value omitted: skipping '{p.displayName}'",
                    )

        new_starts.post(messages)

    def calculate_facility_identifiers(
        self,
        layer,
        layer_short_name: str,
        initials: str,
        start: int,
        interval: int,
        messages: list,
    ) -> str:
        """Return a string with the new facility identifier for a given layer based on its short name, the user's initials,
        the initial value for the number portion of the facility identifier, and the incrementing interval.
        """
        # map of layer short names to prefix, suffix,
        # and whether or not the facility identifier index is calculated for that layer
        layer_kv = {
            "ca_lyr": ("", "CA", True),
            "cv_lyr": ("", "CV", True),
            "ft_lyr": ("", "FT", True),
            "hy_lyr": ("", "HYD", True),
            "sl_lyr": ("", "SERV", False),
            "st_lyr": ("", "STR", False),
            "sv_lyr": ("", "SV", False),
            "wm_lyr": ("000015-WATER-000", "", True),
        }
        # https://pro.arcgis.com/en/pro-app/latest/arcpy/functions/describe.htm
        desc = arcpy.Describe(layer)
        # create absolute path to layer using described layer info
        layer_path = f"{desc.path}\\{desc.name}"
        # unpack values from layer_kv
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
            self.update_err(
                messages,
                "If you see an error that says 'RuntimeError: Cannot acquire a lock.', close the attribute tables of the layers for which you are trying to calculate facility identifiers. If that still does not work, go find whomever wrote this tool and ask them about it.",
            )
        return f"{prefix}{increment}{suffix}"

    def update_warn(self, messages: list, content: str) -> None:
        """Add a warning message, set the progressor label, and update the progressor position."""
        messages.addWarningMessage(content)
        arcpy.SetProgressorLabel(content)
        # Layers have a calculating update_info call and a finished call, so
        # increment by two because this function is called only once when a layer is skipped.
        arcpy.SetProgressorPosition(2)

    def update_info(self, messages: list, content: str) -> None:
        """Add a message, set the progressor label, and update the progressor position."""
        messages.addMessage(content)
        arcpy.SetProgressorLabel(content)
        arcpy.SetProgressorPosition()

    def update_err(self, messages: list, content: str) -> None:
        """Add an error message and raise an ExecutionErorr."""
        messages.addErrorMessage(content)
        raise arcpy.ExecuteError(content)

    class NewStarts:
        def __init__(self) -> None:
            self.starts = {
                "ca_lyr": ["Casing", None],
                "cv_lyr": ["Control Valve", None],
                "ft_lyr": ["Fitting", None],
                "hy_lyr": ["Hydrant", None],
                "sl_lyr": ["Service Line", None],
                "st_lyr": ["Structure", None],
                "sv_lyr": ["System Valve", None],
                "wm_lyr": ["Water Main", None],
            }

        def _create_message(self) -> str:
            """Return a string containing the new facility identifier start values in a human-readable format."""
            message = "New starting values:\n"
            for attr, value in self.starts.items():
                # only add new starts if the value is specified
                if value[1]:
                    message += f"\t{value[0]}: {value[1]}\n"
            return message

        def update(self, layer_short_name: str, new_fid: str) -> None:
            """Update a layer's facility identifier."""
            self.starts[layer_short_name][1] = new_fid

        def post(self, messages: list) -> None:
            """Create a human-readable list of new facility indentifier start values and add a message."""
            messages.addMessage(self._create_message())

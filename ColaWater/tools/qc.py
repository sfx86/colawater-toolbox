import arcpy
import re
import utils


class WaterQualityControl(object):
    def __init__(self) -> None:
        """Initialize tool metadata and capabilities."""
        self.label = "Water Quality Control"
        self.description = (
            "Executes the various quality control checks for water layers."
        )
        self.canRunInBackground = False

    def getParameterInfo(self) -> list[arcpy.Parameter]:
        """Return a list of parameter definitions."""
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

        params = [
            arcpy.Parameter(
                displayName=disp_name,
                name=short_name,
                datatype="GPFeatureLayer",
                parameterType="Optional",
                direction="Input",
            )
            for short_name, disp_name in templates
        ]

        return params

    def updateParameters(self, parameters):
        """Modify parameters to keep them valid. Called every time a parameter is updated."""
        return

    def updateMessages(self, parameters):
        return

    def execute(self, parameters, messages):
        """Tool entry point."""
        casing = parameters[0]
        control_valve = parameters[1]
        fitting = parameters[2]
        hydrant = parameters[3]
        service_line = parameters[4]
        structure = parameters[5]
        system_valve = parameters[6]
        water_main = parameters[7]

        arcpy.SetProgressor(
            "step", "Validating facility identifiers...", 0, 100
        )  # figure out actual max
        status = utils.StatusUpdater(messages)

        # validate fids
        regexes = {
            "ca_lyr": re.compile(r"^\d+CA$"),
            "cv_lyr": re.compile(r"^\d+CV$"),
            "ft_lyr": re.compile(r"^\d+FT$"),
            "hy_lyr": re.compile(r"^\d+HY$"),
            "sl_lyr": re.compile(r"^\d+SL$"),
            "st_lyr": re.compile(r"^\d+ST$"),
            "sv_lyr": re.compile(r"^\d+SERV$"),
            "wm_lyr": re.compile(r"^000015-WATER-000\d+$"),
        }
        with arcpy.da.SearchCursor():
            pass

        return

    def postExecute(self, parameters):
        return
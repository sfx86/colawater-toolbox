import arcpy
import arcpy.conversion

from colawater.lib import desc, tool
from colawater.toolbox.update_ago_data import lib


class UpdateAGOData:
    category = tool.Category.ArcGISOnline.value
    label = "Update AGO Data"
    description = "Downloads layers to be uploaded to ArcGIS Online from aspen."
    canRunInBackground = False

    def execute(self, parameters: list[arcpy.Parameter], messages) -> None:
        conn_aspen = desc.path(parameters[0].value)

        # invariant: parameters[1:] & ExportCategory must have same order
        gdbs = (p.value for p in parameters[1:])
        layer_groups = (l.value for l in lib.ExportCategory)

        with arcpy.EnvManager(workspace=conn_aspen, overwriteOutput=True):
            for layers, gdb in zip(layer_groups, gdbs):
                arcpy.conversion.FeatureClassToGeodatabase(layers, gdb)

    def getParameterInfo(self) -> list[arcpy.Parameter]:
        conn_aspen = arcpy.Parameter(
            displayName="Aspen Connection",
            name="conn_aspen",
            datatype="DEWorkspace",
            parameterType="Required",
            direction="Input",
        )

        gdb_targets = (
            arcpy.Parameter(
                displayName=name_disp,
                name=name,
                datatype="DEWorkspace",
                parameterType="Required",
                direction="Input",
            )
            for name, name_disp in (
                ("gdb_base_data", "BaseData Geodatabase"),
                ("gdb_infrastructure", "Infrastructure Geodatabase"),
                ("gdb_sewer", "Sewer Geodatabase"),
                ("gdb_stormwater", "Stormwater Geodatabase"),
                ("gdb_tables", "Tables Geodatabase"),
                ("gdb_water", "Water Geodatabase"),
            )
        )

        return [conn_aspen, *gdb_targets]

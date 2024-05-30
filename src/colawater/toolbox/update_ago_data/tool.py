import multiprocessing as mp
from typing import Any

import arcpy
import arcpy.conversion

from colawater.lib import desc, tool
from colawater.lib.error import fallible
from colawater.lib.mp import mp_fix_exec

from .lib import FeatureClassGroup, export_to_gdb, gdb_to_zip


@fallible
def gp_worker(conn_aspen: str, gdb: str, fcg: FeatureClassGroup) -> None:
    export_to_gdb(conn_aspen, gdb, fcg)
    gdb_to_zip(gdb)


class UpdateAGOData:
    category = tool.Category.ArcGISOnline.value
    label = "Update AGO Data"
    description = "Downloads layers to be uploaded to ArcGIS Online from aspen."
    canRunInBackground = False

    def execute(self, parameters: list[arcpy.Parameter], messages: list[Any]) -> None:
        arcpy.SetProgressor("default", "Running... (takes ~20min)")

        conn_aspen = desc.full_path(parameters[0].value)

        # invariant:
        # parameters[1:] & ExportCategory must have same order
        gdbs: list[str] = [p.valueAsText for p in parameters[1:]]
        fcgs = [l for l in FeatureClassGroup]

        assert len(gdbs) == len(fcgs)
        arguments = list(zip([conn_aspen] * len(gdbs), gdbs, fcgs))

        mp_fix_exec()
        with mp.Pool(len(arguments)) as pool:
            pool.starmap(gp_worker, arguments)

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

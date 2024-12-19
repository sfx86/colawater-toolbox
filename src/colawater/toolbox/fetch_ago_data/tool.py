import multiprocessing as mp
from typing import Any

import arcpy
import arcpy.conversion

from colawater.lib import desc, tool
from colawater.lib.error import fallible

from .lib import FeatureClassGroup, export_to_gdb, gdb_to_zip


@fallible
def gp_worker(conn_aspen: str, gdb: str, fcg: FeatureClassGroup) -> None:
    export_to_gdb(conn_aspen, gdb, fcg)
    gdb_to_zip(gdb)


class FetchAGOData:
    # category = tool.Category.ArcGISOnline.value
    label = "Fetch AGO Data"
    description = "Fetches layers from aspen and zips them for upload to ArcGIS Online."
    canRunInBackground = False

    def execute(self, parameters: list[arcpy.Parameter], messages: list[Any]) -> None:
        conn_aspen = desc.full_path(parameters[0].value)

        # invariant: parameters[1:] & FeatureClassGroup must have same order
        arguments = [
            (conn_aspen, p.valueAsText, l)
            for p, l in zip(parameters[1:], FeatureClassGroup)
            if p.value is not None
        ]

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
                parameterType="Optional",
                direction="Input",
            )
            for name, name_disp in (
                ("gdb_base_data", "BaseData Geodatabase"),
                ("gdb_infrastructure", "Infrastructure Geodatabase"),
                ("gdb_sewer", "Sewer Geodatabase"),
                ("gdb_stormwater", "Stormwater Geodatabase"),
                ("gdb_tables", "Tables Geodatabase"),
                ("gdb_dpo", "Utility Developer Projects Database"),
                ("gdb_water", "Water Geodatabase"),
            )
        )

        return [conn_aspen, *gdb_targets]

    # fmt: off
    def isLicensed(self) -> bool: return True
    def postExecute(self, parameters: list[arcpy.Parameter]) -> None: pass
    def updateMessages(self, parameters: list[arcpy.Parameter]) -> None: pass
    def updateParameters(self, parameters: list[arcpy.Parameter]) -> None: pass
    # fmt: on

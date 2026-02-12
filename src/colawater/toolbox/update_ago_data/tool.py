import tempfile
import time
from multiprocessing.pool import ThreadPool
from typing import Any, Callable

import arcgis
import arcpy

from colawater.lib import desc

from .lib import *


class UpdateAGOData:
    label = "Update AGO Data"
    description = (
        "Pulls select feature classes from SDE and publishes them to ArcGIS Online."
    )
    canRunInBackground = False

    def execute(self, parameters: list[arcpy.Parameter], messages: list[Any]) -> None:
        conn_aspen = desc.full_path(parameters[0].value)
        conn_portal = arcgis.GIS(parameters[1].valueAsText)
        tag = "auto_weekly_data"
        try:
            # raises a custom FolderException that isn't exposed anywhere
            # if folder exists
            folder = conn_portal.content.folders.create(tag)
        except Exception:
            folder = conn_portal.content.folders.get(tag)
        fcs = [
            base_data,
            infrastructure,
            sewer,
            stormwater,
            utility_developer_projects,
            water,
        ]
        steps = len(fcs)

        def _prog_helper(msg: str) -> None:
            arcpy.SetProgressorPosition()
            arcpy.AddMessage(msg)
            arcpy.SetProgressorLabel(msg)

        with (
            ThreadPool(steps) as pool,
            tempfile.TemporaryDirectory() as tmp_dir,
        ):
            arcpy.SetProgressor("step", min_range=0, max_range=steps, step_value=1)

            def _env(f: Callable) -> Callable:
                def wrapper(*args, **kwargs):
                    with arcpy.EnvManager(
                        workspace=conn_aspen,
                        transferGDBAttributeProperties=True,
                    ):
                        f(*args, **kwargs)

                return wrapper

            _prog_helper("Downloading data...")
            pool.starmap(
                arcpy.management.CreateFileGDB,
                [
                    [tmp_dir for _ in range(steps)],
                    titles,
                ],
            )

            gdbs = [f"{tmp_dir}\\{title}.gdb" for title in titles]

            pool.starmap(
                _env(arcpy.conversion.FeatureClassToGeodatabase),
                [
                    fcs[:-1],
                    gdbs[:-1],
                ],
            )
            _env(
                arcpy.conversion.TableToGeodatabase
            )(  # pyright: ignore [reportAttributeAccessIssue]
                gdbs[-1], f"{tmp_dir}\\Tables.gdb"
            )

            _prog_helper("Compressing geodatabases...")
            pool.starmap(gdb_to_zip, gdbs)

            _prog_helper("Removing remote geodatabases...")
            gdbs_remote = conn_portal.content.search(
                query=f"", item_type="File Geodatabase", filter=f"tags:{tag}"
            )
            # no need for mp, this takes like 2 seconds
            for gdb in gdbs_remote:
                gdb.delete()

            _prog_helper("Uploading geodatabases...")
            gdbs_zipped = [f"{tmp_dir}\\{title}.zip" for title in titles]
            pool.starmap(
                upload_gdb,
                [
                    [folder for _ in range(steps)],
                    gdbs_zipped,
                    titles,
                    [[tag] for _ in range(steps)],
                ],
            )

            _prog_helper("Waiting for publishing availability...")
            while (
                len(
                    gdbs_remote := conn_portal.content.search(
                        query=f"",
                        item_type="File Geodatabase",
                        filter=f"tags:{tag}",
                    )
                )
                < steps
            ):
                time.sleep(1)

            _prog_helper("Publishing feature layers...")
            pool.starmap(publish_gdb, gdbs_remote)

    def getParameterInfo(self) -> list[arcpy.Parameter]:
        conn_aspen = arcpy.Parameter(
            displayName="SDE Connection",
            name="conn_aspen",
            datatype="DEWorkspace",
            parameterType="Required",
            direction="Input",
        )

        conn_portal = arcpy.Parameter(
            displayName="Portal Connection",
            name="conn_portal",
            datatype="GPNetworkDataSource",
            parameterType="Required",
            direction="Input",
        )

        return [conn_aspen, conn_portal]

    # fmt: off
    def isLicensed(self) -> bool: return True
    def postExecute(self, parameters: list[arcpy.Parameter]) -> None: pass
    def updateMessages(self, parameters: list[arcpy.Parameter]) -> None: pass
    def updateParameters(self, parameters: list[arcpy.Parameter]) -> None: pass
    # fmt: on

from pathlib import Path
from typing import Any
from zipfile import ZipFile

import arcpy
from arcgis.gis import ItemProperties, ItemTypeEnum

from colawater.lib.error import fallible

_SPATIAL_REFERENCE = "3361"


class LayerTablePair:
    """
    Paired layers and tables.
    """

    def __init__(
        self,
        name: str,
        feature_classes: list[str],
        tables: list[str],
    ) -> None:
        self.name = name
        self.feature_classes = feature_classes
        self.tables = tables


base_data: LayerTablePair = LayerTablePair(
    "BaseData",
    [
        "SDE.Boundary\\SDE.COC_CITY_LIMIT",
        "SDE.Boundary\\SDE.COUNCIL_DISTRICT",
        "SDE.Boundary\\SDE.COUNTY",
        "SDE.Boundary\\SDE.MUNICIPALITY",
        "SDE.Boundary\\SDE.NEIGHBORHOOD",
        "SDE.Boundary\\SDE.ZIP_CODE",
        "SDE.LandRecords\\SDE.ADDRESS_POINT",
        "SDE.LandRecords\\SDE.PARCEL",
        "SDE.NHDHydrology\\SDE.NHD_FLOWLINE",
        "SDE.NHDHydrology\\SDE.WATER_BODY",
        "SDE.Transportation\\SDE.STREETS",
        "SDE.Transportation\\SDE.TR_RAILROAD",
    ],
    [],
)
infrastructure: LayerTablePair = LayerTablePair(
    "Infrastructure",
    [
        "SDE.InfrastructureOperations\\SDE.Easements",
        "SDE.InfrastructureOperations\\SDE.FOG",
        "SDE.InfrastructureOperations\\SDE.InspectorBoundaryArea",
        "SDE.InfrastructureOperations\\SDE.Laterals",
        "SDE.InfrastructureOperations\\SDE.PACP_Continuous_Defects",
        "SDE.InfrastructureOperations\\SDE.PACP_Pipe_Scores",
        "SDE.InfrastructureOperations\\SDE.PACP_Point_Defects",
        "SDE.InfrastructureOperations\\SDE.RainGauge",
        "SDE.InfrastructureOperations\\SDE.SSO",
        "SDE.InfrastructureOperations\\SDE.SS_ProjectArea",
        "SDE.InfrastructureOperations\\SDE.WM4484_HYDRANTS",
        "SDE.InfrastructureOperations\\SDE.WM4484_VALVES",
        "SDE.InfrastructureOperations\\SDE.ssBasinBoundary",
        "SDE.InfrastructureOperations\\SDE.ssCapacityAssessmentAreas",
        "SDE.InfrastructureOperations\\SDE.ssGravityMain_Criticality_Condition_Scenario3",
        "SDE.InfrastructureOperations\\SDE.ssManagementAreas",
        "SDE.InfrastructureOperations\\SDE.ssMonitoringWell",
        "SDE.InfrastructureOperations\\SDE.ssPermittedIndustry",
        "SDE.InfrastructureOperations\\SDE.ssSatelliteSewer_polygon",
        "SDE.InfrastructureOperations\\SDE.swCriticalityWatersheds",
        "SDE.InfrastructureOperations\\SDE.waCriticalAreas",
        "SDE.InfrastructureOperations\\SDE.waDistributionSites",
        "SDE.InfrastructureOperations\\SDE.waDistrictOffices",
        "SDE.InfrastructureOperations\\SDE.waDistricts",
        "SDE.InfrastructureOperations\\SDE.waPressureZone",
    ],
    [],
)
sewer: LayerTablePair = LayerTablePair(
    "Sewer",
    [
        "SDE.Sewer\\SDE.ssBend",
        "SDE.Sewer\\SDE.ssCasing",
        "SDE.Sewer\\SDE.ssCleanOut",
        "SDE.Sewer\\SDE.ssControlValve",
        "SDE.Sewer\\SDE.ssFitting",
        "SDE.Sewer\\SDE.ssGravityMain",
        "SDE.Sewer\\SDE.ssGravityMain_Deleted",
        "SDE.Sewer\\SDE.ssLateralLine",
        "SDE.Sewer\\SDE.ssManhole",
        "SDE.Sewer\\SDE.ssManhole_Deleted",
        "SDE.Sewer\\SDE.ssNetworkStructure",
        "SDE.Sewer\\SDE.ssPressurizedMain",
        "SDE.Sewer\\SDE.ssPumpStation",
        "SDE.Sewer\\SDE.ssServiceConnection",
        "SDE.Sewer\\SDE.ssSystemValve",
        "SDE.Sewer\\SDE.ssTap",
        "SDE.Sewer\\SDE.ssVault",
    ],
    [
        "SDE.ssEasement_Maintenance",
        "SDE.ssFlowMeters",
        "SDE.ssGravityMain_InspectionSummary",
        "SDE.ssGravityMain_RehabSummary",
        "SDE.ssLateralLine_InspectionSummary",
        "SDE.ssLateralLine_RehabSummary",
        "SDE.ssManhole_InspectionSummary",
        "SDE.ssManhole_RehabSummary",
        "SDE.ssRootControl_WorkSummary",
    ],
)
stormwater: LayerTablePair = LayerTablePair(
    "Stormwater",
    [
        "SDE.StormWater\\SDE.swDischargePoint",
        "SDE.StormWater\\SDE.swDischargePoint_Deleted",
        "SDE.StormWater\\SDE.swDrainPipe",
        "SDE.StormWater\\SDE.swDrainPipe_Deleted",
        "SDE.StormWater\\SDE.swInlet",
        "SDE.StormWater\\SDE.swInlet_Deleted",
        "SDE.StormWater\\SDE.swNaturalWaterbody",
        "SDE.StormWater\\SDE.swNetworkStructure",
        "SDE.StormWater\\SDE.swNetworkStructure_Deleted",
        "SDE.StormWater\\SDE.swOpenDrain",
        "SDE.StormWater\\SDE.swOpenDrain_Deleted",
        "SDE.StormWater\\SDE.swPermBMP",
        "SDE.StormWater\\SDE.swPermBMP_Deleted",
        "SDE.StormWater\\SDE.swVirtualReach",
    ],
    [
        "SDE.swConveyanceCondition",
        "SDE.swConveyance_RehabSummary",
        "SDE.swNodesCondition",
        "SDE.swNodes_RehabSummary",
    ],
)
utility_developer_projects: LayerTablePair = LayerTablePair(
    "UtilityDeveloperProjects",
    [
        "SDE.DataUpdateGP\\SDE.UtilityDeveloperProjects",
    ],
    [],
)
water: LayerTablePair = LayerTablePair(
    "Water",
    [
        "SDE.WaterNetwork\\SDE.waCasing",
        "SDE.WaterNetwork\\SDE.waControlValve",
        "SDE.WaterNetwork\\SDE.waCurbStopValve",
        "SDE.WaterNetwork\\SDE.waFitting",
        "SDE.WaterNetwork\\SDE.waHydrant",
        "SDE.WaterNetwork\\SDE.waHydrant_deleted",
        "SDE.WaterNetwork\\SDE.waMain_Deleted",
        "SDE.WaterNetwork\\SDE.waMeter",
        "SDE.WaterNetwork\\SDE.waNetworkStructure",
        "SDE.WaterNetwork\\SDE.waSamplingStation",
        "SDE.WaterNetwork\\SDE.waServiceLine",
        "SDE.WaterNetwork\\SDE.waStructure",
        "SDE.WaterNetwork\\SDE.waSystemValve",
        "SDE.WaterNetwork\\SDE.waTestStation",
        "SDE.WaterNetwork\\SDE.waWaterMain",
    ],
    [
        "SDE.PRV_RemoteSites",
        "SDE.PS_RemoteSites",
        "SDE.Tank_RemoteSites",
    ],
)


@fallible
def gdb_to_zip(gdb: str) -> None:
    """
    Zips a geodatabase in the same directory as the geodatabase.

    Arguments:
        gdb (str): The path to the target gdb.

    Returns:
        None


    Note:
        Path arguments are str and not Path or arcpy.Parameter because paths inside
        geodatabases aren't real filesystem paths and arcpy.Parameter doesn't pickle.
    """
    target = Path(gdb)

    with ZipFile(target.with_suffix(".zip"), "w") as zip_file:
        for entry in filter(
            # lockfile permissions prevent them from being zipped
            lambda p: p.suffix != ".lock",
            target.rglob("*"),
        ):
            zip_file.write(entry, entry.relative_to(target.parent))


@fallible
def upload_gdb(folder: Any, gdb: Any, title: str, tags: list[str]) -> None:
    """
    Uploads a geodatabase to a folder with a given title and tags.

    Arguments:
        folder (Any): The remote folder.
        remote_gdb (Any): The path to the target gdb.
        title (str): The title to use as the publishing name.
        tags (list[str]): The list of tags to apply to the published item.

    Returns:
        None
    """
    item_properties = ItemProperties(
        title=title,
        item_type=ItemTypeEnum.FILE_GEODATABASE.value,
        spatial_reference=_SPATIAL_REFERENCE,
        tags=tags,
    )

    folder.add(
        item_properties=item_properties,
        file=gdb,
    )


@fallible
def publish_gdb(remote_gdb: Any) -> None:
    """
    Publishes a remote gdb as a feature class service.

    Arguments:
        remote_gdb (Any): The path to the target gdb.

    Returns:
        None
    """
    publish_parameters = {
        "name": remote_gdb.title,
        "targetSR": {
            "wkid": _SPATIAL_REFERENCE,
        },
    }

    remote_gdb.publish(
        publish_parameters=publish_parameters,
        file_type="filegeodatabase",
        overwrite=True,
    )

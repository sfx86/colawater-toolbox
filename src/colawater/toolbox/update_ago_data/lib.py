from enum import Enum, unique
from pathlib import Path
from zipfile import ZipFile

import arcpy


# maybe a better way to organize this data?
# an enum made more sense when not just iter()-ing over it,
# but idk
@unique
class FeatureClassGroup(Enum):
    """
    Groups of feature classes from aspen.
    """

    BaseData = [
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
    ]
    Infrastructure = [
        "SDE.InfrastructureOperations\\SDE.WM4484_VALVES",
        "SDE.InfrastructureOperations\\SDE.Laterals",
        "SDE.InfrastructureOperations\\SDE.SSO",
        "SDE.InfrastructureOperations\\SDE.swCriticalityWatersheds",
        "SDE.InfrastructureOperations\\SDE.WM4484_HYDRANTS",
        "SDE.InfrastructureOperations\\SDE.FOG",
        "SDE.InfrastructureOperations\\SDE.ssSatelliteSewer_polygon",
        "SDE.InfrastructureOperations\\SDE.PACP_Continuous_Defects",
        "SDE.InfrastructureOperations\\SDE.CIPs",
        "SDE.InfrastructureOperations\\SDE.ssManagementAreas",
        "SDE.InfrastructureOperations\\SDE.ssCapacityAssessmentAreas",
        "SDE.InfrastructureOperations\\SDE.waDistrictOffices",
        "SDE.InfrastructureOperations\\SDE.RainGauge",
        "SDE.InfrastructureOperations\\SDE.ssPermittedIndustry",
        "SDE.InfrastructureOperations\\SDE.SS_ProjectArea",
        "SDE.InfrastructureOperations\\SDE.Easements",
        "SDE.InfrastructureOperations\\SDE.PACP_Pipe_Scores",
        "SDE.InfrastructureOperations\\SDE.waPressureZone",
        "SDE.InfrastructureOperations\\SDE.ssGravityMain_Criticality_Condition_Scenario3",
        "SDE.InfrastructureOperations\\SDE.ssBasinBoundary",
        "SDE.InfrastructureOperations\\SDE.ssMonitoringWell",
        "SDE.InfrastructureOperations\\SDE.PACP_Point_Defects",
        "SDE.InfrastructureOperations\\SDE.InspectorBoundaryArea",
        "SDE.InfrastructureOperations\\SDE.waCriticalAreas",
        "SDE.InfrastructureOperations\\SDE.waDistributionSites",
        "SDE.InfrastructureOperations\\SDE.waDistricts",
    ]
    Sewer = [
        "SDE.Sewer\\SDE.ssPumpStation",
        "SDE.Sewer\\SDE.ssManhole",
        "SDE.Sewer\\SDE.ssVault",
        "SDE.Sewer\\SDE.ssBend",
        "SDE.Sewer\\SDE.ssPressurizedMain",
        "SDE.Sewer\\SDE.ssLateralLine",
        "SDE.Sewer\\SDE.ssTap",
        "SDE.Sewer\\SDE.ssServiceConnection",
        "SDE.Sewer\\SDE.ssControlValve",
        "SDE.Sewer\\SDE.ssGravityMain_Deleted",
        "SDE.Sewer\\SDE.ssManhole_Deleted",
        "SDE.Sewer\\SDE.ssSystemValve",
        "SDE.Sewer\\SDE.ssFitting",
        "SDE.Sewer\\SDE.ssCleanOut",
        "SDE.Sewer\\SDE.ssCasing",
        "SDE.Sewer\\SDE.ssNetworkStructure",
        "SDE.Sewer\\SDE.ssGravityMain",
    ]
    Stormwater = [
        "SDE.StormWater\\SDE.swNetworkStructure",
        "SDE.StormWater\\SDE.swDrainPipe",
        "SDE.StormWater\\SDE.swInlet_Deleted",
        "SDE.StormWater\\SDE.swOpenDrain",
        "SDE.StormWater\\SDE.swOpenDrain_Deleted",
        "SDE.StormWater\\SDE.swNetworkStructure_Deleted",
        "SDE.StormWater\\SDE.swDischargePoint",
        "SDE.StormWater\\SDE.swPermBMP",
        "SDE.StormWater\\SDE.swDischargePoint_Deleted",
        "SDE.StormWater\\SDE.swPermBMP_Deleted",
        "SDE.StormWater\\SDE.swVirtualReach",
        "SDE.StormWater\\SDE.swInlet",
        "SDE.StormWater\\SDE.swNaturalWaterbody",
        "SDE.StormWater\\SDE.swDrainPipe_Deleted",
    ]
    Tables = [
        "SDE.PRV_RemoteSites",
        "SDE.PS_RemoteSites",
        "SDE.Tank_RemoteSites",
        "SDE.ssCleanout_RehabSummary",
        "SDE.ssEasement_Maintenance",
        "SDE.ssFlowMeters",
        "SDE.ssGravityMain_InspectionSummary",
        "SDE.ssGravityMain_RehabSummary",
        "SDE.ssLateralLine_InspectionSummary",
        "SDE.ssLateralLine_RehabSummary",
        "SDE.ssManhole_InspectionSummary",
        "SDE.ssManhole_RehabSummary",
        "SDE.ssRootControl_WorkSummary",
        "SDE.swConveyanceCondition",
        "SDE.swNodesCondition",
    ]
    Water = [
        "SDE.WaterNetwork\\SDE.waNetworkStructure",
        "SDE.WaterNetwork\\SDE.waHydrant",
        "SDE.WaterNetwork\\SDE.waSystemValve",
        "SDE.WaterNetwork\\SDE.waServiceLine",
        "SDE.WaterNetwork\\SDE.waTestStation",
        "SDE.WaterNetwork\\SDE.waCurbStopValve",
        "SDE.WaterNetwork\\SDE.waControlValve",
        "SDE.WaterNetwork\\SDE.waWaterMain",
        "SDE.WaterNetwork\\SDE.waMeter",
        "SDE.WaterNetwork\\SDE.waSamplingStation",
        "SDE.WaterNetwork\\SDE.waHydrant_deleted",
        "SDE.WaterNetwork\\SDE.waStructure",
        "SDE.WaterNetwork\\SDE.waCasing",
        "SDE.WaterNetwork\\SDE.waFitting",
        "SDE.WaterNetwork\\SDE.waMain_Deleted",
    ]


def export_to_gdb(conn_aspen: str, gdb: str, fcg: FeatureClassGroup) -> None:
    """
    Exports the layers from the FeatureClass group to gdb from conn_aspen.

    Arguments:
        conn_aspen (str): The path to the aspen connection.
        gdb (str): The path to the target gdb.
        fcg (FeatureClassGroup): The group of feature classes to export.

    Returns:
        None

    Note:
        Path arguments are str and not Path or arcpy.Parameter because paths inside
        geodatabases aren't real filesystem paths and arcpy.Parameter doesn't pickle.
    """
    with arcpy.EnvManager(
        workspace=conn_aspen,
        overwriteOutput=True,
        transferGDBAttributeProperties=True,
    ):
        if fcg == FeatureClassGroup.Tables:
            arcpy.conversion.TableToGeodatabase(  # pyright: ignore [reportAttributeAccessIssue]
                fcg.value, gdb
            )
        else:
            arcpy.conversion.FeatureClassToGeodatabase(  # pyright: ignore [reportAttributeAccessIssue]
                fcg.value, gdb
            )


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

    with ZipFile(target.with_suffix(".gdb.zip"), "w") as zip_file:
        for entry in target.rglob("*"):
            zip_file.write(entry, entry.relative_to(target.parent))

import arcpy


def get_layer_path(layer) -> str:
    """Return an absolute path to a layer."""
    # https://pro.arcgis.com/en/pro-app/latest/arcpy/functions/describe.htm
    desc = arcpy.Describe(layer)
    # create absolute path to layer using described layer info
    return f"{desc.path}\\{desc.name}"

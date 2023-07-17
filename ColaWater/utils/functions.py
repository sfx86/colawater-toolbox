import arcpy


def get_layer_path(layer: arcpy._mp.Layer) -> str:
    """Return an absolute path to a layer."""
    desc = arcpy.Describe(layer)
    return f"{desc.path}\\{desc.name}"

import arcpy
from colawater import utils
from functools import cache


def get_layer_path(layer: arcpy._mp.Layer) -> str:
    """Return an absolute path to a layer."""
    desc = arcpy.Describe(layer)
    return f"{desc.path}\\{desc.name}"


@cache
def is_existing_scan(filename: str) -> bool:
    """Return true if the given string is a valid scan filename."""
    # this function is extremely hot and many of the arguments are identical, hence
    # the @cache decorator
    # if the amount of filenames processed ever gets particularly high,
    # consider changing to @lru_cache(n) to deal with memory issues

    # takes advantage of short-circuiting to avoid filesystem ops where possible
    return bool(filename) and (
        (
            # valid scans only ever have these extensions
            # and appear in this order of frequency
            filename.endswith(".tif")
            or filename.endswith(".pdf")
            or filename.endswith(".dwg")
        )
        and (utils.SCAN_DIR / filename).exists()
    )


def process_attr(attr: str, csv: bool = False) -> str:
    """Return a more understandable representation of a nullable field value and
    optionally make it more easily ingested into a CSV."""
    # only check for none as empty strings are also falsy and
    # naming those <Null> would cause confusion
    if attr is None:
        return "<Null>"
    elif csv:
        # some fields have erroneous whitespace or contain commas or quotes
        # remove these to make use as csv possible
        return attr.strip().replace(",", "").replace('"', "")

    return attr

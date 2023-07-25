"""
A collection of functions common to and useful in many tools.

Examples:
    .. code-block:: python

        layer = layer_from_somewhere()
        path = get_layer_path(layer) # Returns "path/to/layer"

    .. code-block:: python

        filename = "foo"
        if is_existing_scan(filename):
            do_something()

    .. code-block:: python

        attr = None
        attr = process_attr(attr) # Returns "<Null>"
"""

import arcpy
from colawater import utils
from functools import cache


def get_layer_path(layer: arcpy._mp.Layer) -> str:
    """
    Returns the absolute path to a layer.

    Uses ``arcpy.Describe(layer)`` to get layer information and build a path.

    Arguments:
        layer (arcpy._mp.Layer): A layer object.

    Returns:
        str: The absolute path to the layer.
    """
    desc = arcpy.Describe(layer)
    return f"{desc.path}\\{desc.name}"


@cache
def is_existing_scan(filename: str) -> bool:
    """
    Returns whether this scan file exists.

    Applies some heuristics to detect if the string is a valid
    scan file name and only checks the filesystem if those heuristics pass.
    Caches arguments and results to avoid erroneous filesystem accesses.

    Arguments:
        filename (str): The name of a file.

    Returns:
        bool: Whether a scan with ``filename`` exists.
    """
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
    """
    Returns a human readable string representation of a nullable field value.

    Turns a ``None`` value into ``"<Null>"`` and optionally strips out whitespace,
    commas, and quotation marks.
    Return a more understandable representation of a nullable field value and
    optionally make it more easily ingested into a CSV.

    Arguments:
        attr (str): The attribute value to be processed.
        csv (bool): Whether to apply CSV pre-processing.

    Returns:
        str: The processed attribute value.
    """
    # only check for none as empty strings are also falsy and
    # naming those <Null> would cause confusion
    attr = str(attr)
    if attr is None:
        return "<Null>"
    elif csv:
        # some fields have erroneous whitespace or contain commas or quotes
        # remove these to make use as csv possible
        return attr.strip().replace(",", "").replace('"', "")

    return attr

"""
Utilities for handling attribute values.

Examples:
    .. code-block:: python

        import colawater.attribute as attr

        foo = None
        foo = attr.process(foo) # Returns "<Null>".
"""
from typing import Optional, Union

CSV_PROCESSING_MSG: str = "Commas, leading and trailing whitespace, and quotation marks have been removed so this output can be consumed properly as a CSV."
"""
Message text to display when the following output has been modified for CSV use.
"""


def process(attr: Optional[Union[str, int]], csv: bool = False) -> str:
    """
    Returns a human readable string representation of a nullable field value.

    Turns a ``None`` value into ``"<Null>"`` and optionally strips out whitespace,
    commas, and quotation marks for ease of use as a CSV.

    Arguments:
        attr (Optional[Union[str, int]]): The attribute value to be processed.
        csv (bool): Whether to apply CSV pre-processing.

    Returns:
        str: The processed attribute value.
    """
    # only check for none as empty strings are also falsy and
    # naming those <Null> would cause confusion
    if attr is None:
        return "<Null>"

    attr = str(attr)  # convert other possible types to str
    if csv:
        return attr.strip().replace(",", "").replace('"', "")

    return attr

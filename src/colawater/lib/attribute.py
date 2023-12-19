"""
Functions for working with attribute values.

Examples:
    .. code-block:: python

        foo = None
        foo = process(foo) # Returns "<Null>".
        
        bar = "      whitespace example   \n\n"
        bar = process(bar) # Returns "whitespace example"
"""
from typing import Any, Optional


def process(attr: Optional[Any]) -> Any:
    """
    Turns a ``None`` (null in ArcGIS) value into ``"<Null>"``.

    Arguments:
        attr (Optional[Any]): The attribute value to be processed.

    Returns:
        str: The processed attribute value.
    """
    if attr is None:
        return "<Null>"

    return attr

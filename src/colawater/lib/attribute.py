"""
Functions for working with attribute values.

Examples:
    .. code-block:: python

        foo = None
        foo = process(foo) # Returns "<Null>".
"""

from typing import Any, Optional


def to_str(attr: Optional[Any]) -> str:
    """
    Calls ``str`` with the argument or turns a ``None`` (null in ArcGIS) value into ``"<Null>"``.

    Arguments:
        attr (Optional[Any]): The attribute value to be processed.

    Returns:
        str: The processed attribute value.
    """
    if attr is None:
        return "<Null>"

    return str(attr)

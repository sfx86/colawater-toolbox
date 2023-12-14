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


def process(attr: Optional[Any]) -> str:
    """
    Returns a human readable string representation of a nullable field value.

    Turns a ``None`` value into ``"<Null>"`` and optionally strips leading and trailing whitespace.

    Arguments:
        attr (Optional[Any]): The attribute value to be processed.

    Returns:
        str: The processed attribute value.
    """
    # only check for none as empty strings are also falsy,
    # so naming those <Null> would be incorrect
    if attr is None:
        processed_attr = "<Null>"
    else:
        processed_attr = str(attr).strip()

    return processed_attr

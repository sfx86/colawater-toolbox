"""
A convenience decorator for initializing the arcpy progressor.

Examples:
    .. code-block:: python

        from colawater.progressor import progressor

        @progressor("helpful message")
        def f() -> None:
            do_something()
"""
from functools import wraps
from typing import Any, Callable, TypeVar

import arcpy

_T = TypeVar("_T")


def progressor(label: str) -> Callable[[Callable[..., _T]], Callable[..., _T]]:
    """
    Wraps the decorated function and prefixes it with boilerplate progressor setup.

    Arguments:
        label (str): The progressor label.
    """

    def decorator(f: Callable[..., _T]) -> Callable[..., _T]:
        @wraps(f)
        def wrapper(*args: Any, **kwargs: Any) -> _T:
            arcpy.SetProgressor("default", label)
            return f(*args, **kwargs)

        return wrapper

    return decorator

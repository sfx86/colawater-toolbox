"""
Type factory for building arcpy tools.

Examples:
    .. code-block:: python
    
        from magic import Wizard

        Foo = toolshed(Wizard)

"""
from enum import Enum, unique
from functools import wraps
from typing import Any, Callable, TypeVar

import arcpy


@unique
class Category(Enum):
    CheckIn = "Check-in"
    Tools = "Tools"
    QualityControl = "Quality Control"


_T = TypeVar("_T")


def entry(tool_name: str) -> Callable[[Callable[..., _T]], Callable[..., _T]]:
    """
    Wraps the decorated function and prefixes it with boilerplate progressor setup.

    Arguments:
        tool_name (str): The tool name of the entry point being annotated.
    """

    def decorator(f: Callable[..., _T]) -> Callable[..., _T]:
        @wraps(f)
        def wrapper(*args: Any, **kwargs: Any) -> _T:
            arcpy.SetProgressor("default", f"Running {tool_name}")
            return f(*args, **kwargs)

        return wrapper

    return decorator


def label(name: str, category: Category) -> str:
    """
    Formats a tool label.

    Arguments:
        name (str): The tool name.
        category (Category): The tool category.

    Returns:
        str: The formatted name.
    """
    return f"{name} ({category.value})"

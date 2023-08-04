from functools import wraps
from typing import Any, Callable, NoReturn, Optional, TypeVar, Union

import arcpy

import colawater.status.logging as log
import colawater.status.summary as sy

RUNTIME_ERROR_MSG: str = "\n".join(
    (
        "How to resolve common errors:",
        "'RuntimeError: An expected Field was not found or could not be retrieved properly.'",
        "\tYou probably selected the wrong layer in the dropdown.",
        "'RuntimeError: Attribute column not found'",
        "\tYou probably selected the wrong layer in the dropdown.",
        "'RuntimeError: Cannot acquire a lock.',",
        "\tClose the attribute tables of the layers with which you are trying to use this tool.",
        "'RuntimeError: Objects in this class cannot be updated outside an edit session'",
        "\tYou probably selected a layer from cypress by mistake.",
    )
)
"""
Error message text to display on ``RuntimeError``.
"""

UNEXPECTED_ERROR_MSG: str = "\n".join(
    (
        "An unexpected error occurred :(",
        "Go find whomever wrote this tool and ask them about it.",
    )
)
"""
Error message text to display on ``Exception``.
"""


T = TypeVar("T")


def fallible(f: Callable[..., T]) -> Callable[..., Union[T, NoReturn]]:
    """
    Wraps the decorated function in a try-catch block that handles
    ``RuntimeError`` and ``Exception``, dumping the tool summary
    and printing a relevant error message if either exception is raised.

    Returns:
        Union[T, NoReturn]: The return value of the wrapped function, or an exception is caught,
                            an ``ExecuteError`` is raised and the function does not return.

    Raises:
        ExecuteError: An exception was caught, so this was raised in its place.
    """

    @wraps(f)
    def wrapper(*args, **kwargs) -> Union[T, NoReturn]:
        try:
            res: T = f(*args, **kwargs)
            return res
        except RuntimeError:
            sy.post(dumped=True)
            log.error(RUNTIME_ERROR_MSG)
            raise arcpy.ExecuteError
        except Exception:
            sy.post(dumped=True)
            log.error(UNEXPECTED_ERROR_MSG)
            raise arcpy.ExecuteError

    return wrapper

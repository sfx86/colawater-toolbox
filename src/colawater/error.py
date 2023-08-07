import inspect
from functools import wraps
from typing import Any, Callable, NoReturn, Optional, TypeVar, Union

import arcpy

import colawater.status.logging as log
import colawater.status.summary as sy

SYSTEM_ERROR_MSG: str = """How to resolve common errors:
'RuntimeError: An expected Field was not found or could not be retrieved properly.'
    You probably selected the wrong layer in the dropdown.
'RuntimeError: Attribute column not found'
    You probably selected the wrong layer in the dropdown.
'RuntimeError: Cannot acquire a lock.'
    Close the attribute tables of the layers with which you are trying to use this tool.
'RuntimeError: Objects in this class cannot be updated outside an edit session'
    You probably selected a layer from cypress by mistake.
"""
"""
Error message text to display on ``SystemError``

Note:
    The error message output almost always says 'RuntimeError' when a SystemError occurs.
"""

UNEXPECTED_ERROR_MSG: str = """An unexpected error occurred :(
Go find whomever wrote this tool and ask them about it."""
"""
Error message text to display on ``Exception`` (not including ``SystemError``).
"""


T = TypeVar("T")


def fallible(f: Callable[..., T]) -> Callable[..., Union[T, NoReturn]]:
    """
    Wraps the decorated function in a try-catch block that handles
    ``RuntimeError`` and ``Exception``, dumping the tool summary
    and printing a relevant error message if either exception is raised.

    Returns:
        Union[T, NoReturn]: The return value of the wrapped function, or an exception is caught,
                            an ``ExecuteError`` is raised, and the function does not return.

    Raises:
        ExecuteError: An exception was caught, so this was raised in its place.
    """

    @wraps(f)
    def wrapper(*args: Any, **kwargs: Any) -> Union[T, NoReturn]:
        def post_log_exit(err: BaseException, msg: str) -> NoReturn:
            sy.post(dumped=True)
            log.error(f"Error: {type(err).__name__}\n{msg}")
            raise arcpy.ExecuteError

        try:
            res: T = f(*args, **kwargs)
        except SystemError as err:
            post_log_exit(err, SYSTEM_ERROR_MSG)
        except Exception as err:
            post_log_exit(err, UNEXPECTED_ERROR_MSG)
        else:
            return res

    return wrapper

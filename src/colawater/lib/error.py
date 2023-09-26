"""
Functions for handling errors from arcpy.

Examples:
    .. code-block:: python

        import arcpy

        @fallible
        def foo(bar: str) -> str:
            if magic_variable:
                raise arcpy.ExecuteError # Caught and handled by decorator
            elif more_magic:
                raise SystemError        # Also caught
            elif magic_again:
                raise RuntimeError       # Catches this too!
            
            return bar # This is returned normally
"""
from functools import wraps
from typing import Any, Callable, NoReturn, TypeVar, Union

import arcpy

from . import summary as sy

EXPECTED_ERROR_MSG: str = """How to resolve common errors:
'RuntimeError: An expected Field was not found or could not be retrieved properly.'
'RuntimeError: Attribute column not found'
    You probably selected the wrong layer in the dropdown.
'RuntimeError: Cannot acquire a lock.'
    Close the attribute tables of the layers with which you are trying to use this tool.
    Another open ArcGIS process could also have a lock on the data, so check for that too.
'RuntimeError: Objects in this class cannot be updated outside an edit session'
    You probably selected a write-protected layer from cypress by mistake.
"""
"""
Error message text to display on ``SystemError`` and ``RuntimeError``.
"""

UNEXPECTED_ERROR_MSG: str = """An unexpected error occurred :(
Go find whomever wrote this tool and ask them about it."""
"""
Error message text to display on non-handled exceptions.
"""


_T = TypeVar("_T")


def fallible(f: Callable[..., _T]) -> Callable[..., Union[_T, NoReturn]]:
    """
    Wraps the decorated function in a try-catch block that handles ``SystemError``/``RuntimeError`` and ``Exception``

    Dumps the tool summary and prints a relevant error message depending on the exception.

    Note:
        The default error message output in ArcGIS often says 'RuntimeError'
        when a SystemError occurs.

    Returns:
        Union[_T, NoReturn]: The return value of the wrapped function.
        Or, if an exception is caught, an ``ExecuteError`` is raised, and the function does not return.

    Raises:
        ExecuteError: An exception was caught, so this was raised in its place.
    """

    @wraps(f)
    def wrapper(*args: Any, **kwargs: Any) -> Union[_T, NoReturn]:
        try:
            res: _T = f(*args, **kwargs)
        except (SystemError, RuntimeError) as err:
            halt(err, EXPECTED_ERROR_MSG)
        except Exception as err:
            halt(err, UNEXPECTED_ERROR_MSG)
        else:
            return res

    return wrapper


def halt(err: Exception, msg: str) -> NoReturn:
    """
    Posts the current summary, raises an ExecuteError, and adds an error message.

    Arguments:
        err (Exception): The exception causing the halt.
        msg (str): The message to supply to the exception.
    """
    sy.post(dumped=True)
    arcpy.AddError(f"Error: {repr(err)}\n{msg}")
    raise arcpy.ExecuteError

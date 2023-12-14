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
            elif magic_again_2:
                raise BaseException      # Uncaught, above Exception in the exception hierarchy
            
            return bar # This is returned normally
"""
from functools import wraps
from typing import Any, Callable, NoReturn, TypeVar, Union

import arcpy

_ERROR_MESSAGE: str = """How to resolve common errors:
'RuntimeError: An expected Field was not found or could not be retrieved properly.'
'RuntimeError: Attribute column not found'
    You probably selected the wrong layer in the dropdown.
'RuntimeError: Cannot acquire a lock.'
    Close the attribute tables of the layers with which you are trying to use this tool.
    Another open ArcGIS process could also have a lock on the data, so check for that too.
'RuntimeError: Objects in this class cannot be updated outside an edit session'
    You probably selected a write-protected layer from cypress by mistake.

If the above solutions do not work, or the error message itself is unhelpful, an unexpected error occurred :(
Go find whomever wrote this tool and ask them about it.
"""
"""
Error message text to display to the user.
"""


_T = TypeVar("_T")


def fallible(f: Callable[..., _T]) -> Callable[..., Union[_T, NoReturn]]:
    """
    Wraps the decorated function in a try-catch block that prints an error message and re-raises ``arcpy.ExecuteError``.

    Returns:
        Union[_T, NoReturn]: The return value of the wrapped function.

    Raises:
        ExecuteError: An exception was caught, so this was raised in its place.
    """

    @wraps(f)
    def wrapper(*args: Any, **kwargs: Any) -> Union[_T, NoReturn]:
        try:
            res: _T = f(*args, **kwargs)
        except Exception as err:
            arcpy.AddError(f"Error: {repr(err)}\n{_ERROR_MESSAGE}")
            raise arcpy.ExecuteError
        else:
            return res

    return wrapper

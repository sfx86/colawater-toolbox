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
    ArcGISOnline = "ArcGIS Online Tools"
    CheckIn = "Check-in Tools"
    CheckOut = "Checkout Tools"
    QualityControl = "Quality Control Tools"

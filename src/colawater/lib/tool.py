"""
Types for tools.

Examples:
    .. code-block:: python
    
        class T():
            category = Category.CheckIn.value

            # etc.

"""

from enum import Enum, unique


@unique
class Category(Enum):
    ArcGISOnline = "ArcGIS Online Tools"
    CheckIn = "Check-in Tools"
    CheckOut = "Checkout Tools"
    QualityControl = "Quality Control Tools"

"""
Utilities for working with scan files.

Examples:
    .. code-block:: python
    
        from colawater import scan

        for file in (f for f in scan.CITY_DIR.iterdir() if scan.exists(f)):
            do_something(file)
"""
from functools import cache
from pathlib import Path

CITY_DIR: Path = Path("M:\\Util&Eng\\Dept_Staff\\Scans\\")
"""
Known static location of city scan directory.
"""

CW2020_DIR: Path = Path(
    "R:\\Projects\\Active\\CW2020_Master\\Source\\RecordDrawings\\Phong\\Scans\\"
)
"""
Known static location of CleanWater 2020 scan directory.
"""


@cache
def exists(filename: str) -> bool:
    """
    Returns whether this scan file exists.

    Applies some heuristics to detect if the string is a valid
    scan file name and only checks the filesystem if those heuristics pass.
    Uses an unbounded LRU cache to store arguments and results to avoid erroneous filesystem accesses.

    Arguments:
        filename (str): The name of a file.

    Returns:
        bool: Whether a scan with ``filename`` exists.
    """
    # this function is extremely hot and many of the arguments
    # are identical, hence the @cache decorator
    # if the amount of filenames processed ever gets particularly high,
    # consider changing to @lru_cache(n) to deal with memory issues

    # takes advantage of short-circuiting to avoid filesystem ops where possible
    return bool(filename) and (
        (
            # valid scans only ever have these extensions
            # and appear in this order of frequency
            filename.endswith(".tif")
            or filename.endswith(".pdf")
            or filename.endswith(".dwg")
        )
        and (CITY_DIR / filename).exists()
    )

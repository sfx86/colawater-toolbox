"""
Wrapper functions for working with arcpy and multiprocessing.
"""

import multiprocessing as mp
import os
import sys


def mp_fix_exec() -> None:
    """
    Fixes the multiprocessing executable that ArcGIS Pro sets incorrectly.


    Multiprocessing tries to use ArcGISPro.exe to handle the new processes, drowning the host system in new arcgis pro instances.
    The solution is to tell multiprocessing to not do that and instead use the GUI python to do the multiprocessing stuff instead.
    ``pythonw.exe`` conveniently doesn't spawn a bunch of blank terminal windows, unlike ``python.exe``.

    https://community.esri.com/t5/python-questions/multiprocessing-using-script-tool-in-pro/m-p/415714/highlight/true#M32752

    Returns:
        None
    """
    mp.set_executable(os.path.join(sys.exec_prefix, "pythonw.exe"))

import multiprocessing as mp
import os
import sys


def mp_fix_exec() -> None:
    # https://community.esri.com/t5/python-questions/multiprocessing-using-script-tool-in-pro/m-p/415714/highlight/true#M32752
    #
    # multiprocessing tries to use ArcGISPro.exe to handle the new processes,
    # drowning the host system in new arcgis pro instances
    # the solution is to tell multiprocessing to not do that and instead use the gui python
    # to do the multiprocessing stuff instead
    # pythonw.exe conveniently doesn't spawn a bunch of blank terminal windows, unlike python.exe
    mp.set_executable(os.path.join(sys.exec_prefix, "pythonw.exe"))

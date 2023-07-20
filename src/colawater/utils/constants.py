from pathlib import Path

# known directories
SCAN_DIR: Path = Path("M:\\Util&Eng\\Dept_Staff\\Scans\\")

# boilerplate messages
RUNTIME_ERROR_MSG: str = "\n".join(
    (
        "How to resolve common errors:",
        "For 'RuntimeError: An expected Field was not found or could not be retrieved properly.', you probably selected the wrong layer in the dropdown.",
        "For 'RuntimeError: Attribute column not found', you probably selected the wrong layer in the dropdown.",
        "For 'RuntimeError: Cannot acquire a lock.', close the attribute tables of the layers with which you are trying to use this tool.",
        "For 'RuntimeError: Objects in this class cannot be updated outside an edit session', you probably selected a layer from cypress by mistake.",
        "If these solutions do not work or you see a different error, go find whomever wrote this tool and ask them about it.",
    )
)

CSV_PROCESSING_MSG: str = "Note: commas, leading and trailing whitespace, and quotation marks have been removed so this output can be consumed properly as a CSV."

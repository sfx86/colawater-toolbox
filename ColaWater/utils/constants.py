RUNTIME_ERROR_MSG = " ".join(
    (
        "If you see an error that says 'RuntimeError: Cannot acquire a lock.', close the attribute tables of the layers with which you are trying to use this tool.",
        "If you see an error that says 'RuntimeError: Objects in this class cannot be updated outside an edit session', you probably selected a layer from cypress by mistake.",
        "If changing these things does not work or you see a different error, go find whomever wrote this tool and ask them about it.",
    )
)
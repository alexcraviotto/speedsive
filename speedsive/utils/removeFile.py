import os


def removeFile(path: str):
    """Remove the file from the given path.

    Args:
        path (str)
    """
    os.remove(path)

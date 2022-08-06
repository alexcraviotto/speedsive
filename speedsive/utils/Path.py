import os


def reducePath(srcPath: str, n: int) -> str:
    """Reduce to n levels above the path.\n
    Args:
        srcPath(str):
        dir(str):
    Returns:
        str:
    """
    return "\\".join(srcPath.split("\\")[:-n])

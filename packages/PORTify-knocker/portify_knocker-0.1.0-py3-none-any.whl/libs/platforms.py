from sys import platform


def is_running_on_windows() -> bool:
    return platform == "win32"


def is_running_on_linux() -> bool:
    return platform == "linux"

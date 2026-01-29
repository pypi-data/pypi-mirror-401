"""ctypes shared library demo helpers."""

from typing import Any

__all__ = ["main"]


def main() -> Any:
    from . import hello_ctypes

    return hello_ctypes.main()

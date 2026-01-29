"""Learning demos for TCP/TLS, HTTP, and SSH."""

import importlib
from typing import Any

__all__ = ["ctypes_shared", "hello_ext", "tcp_tls"]


def __getattr__(name: str) -> Any:
    if name in __all__:
        return importlib.import_module(f"{__name__}.{name}")
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")

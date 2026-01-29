import importlib

import pytest


def test_package_imports() -> None:
    pkg = importlib.import_module("new_year_2026")
    assert hasattr(pkg, "tcp_tls")
    assert hasattr(pkg, "ctypes_shared")


def test_tcp_tls_module_import() -> None:
    mod = importlib.import_module("new_year_2026.tcp_tls")
    assert hasattr(mod, "__doc__")


def test_hello_ext_optional() -> None:
    try:
        hello_ext = importlib.import_module("new_year_2026.hello_ext")
    except ImportError:
        pytest.skip("hello_ext extension not built")
    assert hasattr(hello_ext, "add")
    assert hasattr(hello_ext, "mul")

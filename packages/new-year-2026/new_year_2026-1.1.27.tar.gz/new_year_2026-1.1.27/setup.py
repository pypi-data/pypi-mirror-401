from setuptools import Extension, setup

try:
    import pybind11
except ImportError as exc:
    raise RuntimeError("pybind11 is required to build this extension") from exc


ext_modules = [
    Extension(
        "new_year_2026.hello_ext._core",
        sources=[
            "src/new_year_2026/hello_ext/bindings.cpp",
            "src/new_year_2026/hello_ext/hello_c.c",
            "src/new_year_2026/hello_ext/hello_cpp.cpp",
        ],
        include_dirs=["src/new_year_2026/hello_ext", pybind11.get_include()],
        language="c++",
    )
]

setup(ext_modules=ext_modules)

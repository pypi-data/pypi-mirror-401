#include <pybind11/pybind11.h>

#include "hello_c.h"
#include "hello_cpp.h"

namespace py = pybind11;

PYBIND11_MODULE(_core, m) {
    m.doc() = "pybind11 demo module";
    m.def("add", &add_ints, "Add two integers.");
    m.def("mul", &mul_longs, "Multiply two integers.");
}

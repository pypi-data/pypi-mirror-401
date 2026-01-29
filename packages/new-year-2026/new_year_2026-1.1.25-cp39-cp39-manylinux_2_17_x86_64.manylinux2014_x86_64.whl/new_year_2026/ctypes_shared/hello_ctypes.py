import ctypes
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))

if sys.platform.startswith("win"):
    lib_name = "hello.dll"
elif sys.platform == "darwin":
    lib_name = "libhello.dylib"
else:
    lib_name = "libhello.so"

lib_path = os.path.join(HERE, lib_name)
if not os.path.exists(lib_path):
    raise FileNotFoundError(f"shared library not found: {lib_path}")

def main() -> None:
    lib = ctypes.CDLL(lib_path)
    lib.add_ints.argtypes = [ctypes.c_int, ctypes.c_int]
    lib.add_ints.restype = ctypes.c_int
    lib.hello.argtypes = []
    lib.hello.restype = ctypes.c_char_p

    print("add_ints(2, 3) =", lib.add_ints(2, 3))
    print("hello() =", lib.hello().decode("utf-8"))


if __name__ == "__main__":
    main()

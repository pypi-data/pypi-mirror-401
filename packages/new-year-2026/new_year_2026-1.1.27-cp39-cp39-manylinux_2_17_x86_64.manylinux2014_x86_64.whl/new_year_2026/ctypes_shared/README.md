# ctypes + shared library demo

This example builds a small C shared library and loads it with `ctypes`.

## Build the shared library

macOS:

```bash
cc -shared -fPIC -o libhello.dylib hello.c
```

Linux:

```bash
cc -shared -fPIC -o libhello.so hello.c
```

Windows (MSVC Developer Prompt):

```bat
cl /LD hello.c /Fe:hello.dll
```

## Run the Python demo

```bash
python hello_ctypes.py
```

#!/usr/bin/env bash
set -euo pipefail

demo_dir="${1:?usage: build_ctypes_shared.sh <ctypes_shared_dir>}"

if [[ "$(uname -s)" == "Darwin" ]]; then
  cc -dynamiclib -o "${demo_dir}/libhello.dylib" "${demo_dir}/hello.c"
else
  cc -shared -fPIC -o "${demo_dir}/libhello.so" "${demo_dir}/hello.c"
fi

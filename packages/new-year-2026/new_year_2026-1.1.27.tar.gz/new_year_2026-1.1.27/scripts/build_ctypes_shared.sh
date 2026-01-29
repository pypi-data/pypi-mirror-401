#!/usr/bin/env bash
set -euo pipefail

demo_dir="${1:?usage: build_ctypes_shared.sh <ctypes_shared_dir>}"

if [[ "$(uname -s)" == "Darwin" ]]; then
  out="${demo_dir}/libhello.dylib"
  arm_tmp="${demo_dir}/.libhello_arm64.dylib"
  x86_tmp="${demo_dir}/.libhello_x86_64.dylib"

  if cc -arch arm64 -dynamiclib -o "$arm_tmp" "${demo_dir}/hello.c" && \
     cc -arch x86_64 -dynamiclib -o "$x86_tmp" "${demo_dir}/hello.c"; then
    lipo -create -output "$out" "$arm_tmp" "$x86_tmp"
    rm -f "$arm_tmp" "$x86_tmp"
  else
    cc -dynamiclib -o "$out" "${demo_dir}/hello.c"
  fi
else
  cc -shared -fPIC -o "${demo_dir}/libhello.so" "${demo_dir}/hello.c"
fi

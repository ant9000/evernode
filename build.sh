#!/bin/bash -e

cd "$(dirname $0)"
BASE="`pwd`"
TARGET="${BASE}/build"

which west || {
  echo "West command not found - please activate Zephyr environment"
  exit 1
}

cd "$(dirname $(which west))"
cd "$(west topdir)"

EXTRA_CFLAGS="-DMICROPY_PY_SELECT=1 -DMICROPY_PY_ASYNCIO=1"
#EXTRA_CFLAGS="$EXTRA_CFLAGS -DMICROPY_PY_BLUETOOTH_ENABLE_CENTRAL_MODE=1"
EXTRA_CFLAGS="$EXTRA_CFLAGS -DMICROPY_PY_OS_DUPTERM=1"
EXTRA_CFLAGS="$EXTRA_CFLAGS -DMODULE_HYDROGEN_ENABLED=1"
EXTRA_CFLAGS="$EXTRA_CFLAGS -DMICROPY_EMIT_THUMB=1"

west build -b apollo3_evb \
    -d "$TARGET" \
    --extra-conf "$BASE/evernode.conf" \
    --extra-conf "$BASE/micropython.conf" \
    --extra-dtc-overlay "$BASE/evernode.overlay" \
    "$BASE/micropython/ports/zephyr/" \
    -DUSER_C_MODULES="${BASE}/modules/" \
    -DEXTRA_CFLAGS="$EXTRA_CFLAGS" \
    $*

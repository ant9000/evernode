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

EXTRA_CFLAGS="-DCONFIG_MICROPY_CONFIG_ROM_LEVEL_EXTRA_FEATURES"
EXTRA_CFLAGS="$EXTRA_CFLAGS -DMICROPY_PY_SELECT=1 -DMICROPY_PY_ASYNCIO=1"
EXTRA_CFLAGS="$EXTRA_CFLAGS -DMODULE_HYDROGEN_ENABLED=1"

west build -b apollo3_evb \
    -d "$TARGET" \
    "$BASE/micropython/ports/zephyr/" \
    -DEXTRA_CONF_FILE="$BASE/evernode.conf" \
    -DEXTRA_DTC_OVERLAY_FILE="$BASE/evernode.overlay" \
    -DUSER_C_MODULES="${BASE}/modules/" \
    -DEXTRA_CFLAGS="$EXTRA_CFLAGS" \
    $*

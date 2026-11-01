# INSTALLATION #
Clone this repo first:

```
git clone --recurse-submodules https://github.com/ant9000/evernode
cd evernode
```

Clone Micropython repo:

```
git clone --recurse-submodules https://github.com/ant9000/micropython --branch=devel
```

Install the Zephyr framework, following the [official guide](https://docs.zephyrproject.org/latest/develop/getting_started/index.html). Assuming the default paths of the guide, add a new remote and update:

```
cd ~/zephyrproject/zephyr
# add my remote
git remote add ant9000 https://github.com/ant9000/zephyr
git pull --all
# switch to my devel branch
git checkout -b devel --track ant9000/devel
# bring the framework up to date
source ~/zephyrproject/.venv/bin/activate
west update
west packages pip --install
west sdk install -b ~/zephyrproject/
```

# COMPILATION AND FLASHING #

Remember that Zephyr framework needs to be active when compiling or flashing:

```
source ~/zephyrproject/.venv/bin/activate
```

Compiling the firmware is handled by `build.sh` script:

```
./build.sh
```

For a clean compilation:
```
./build.sh --pristine
```

Two snippets are available: `bt` and `mspi` (the latter is still WIP). To
enable Bluetooth, for instance, you can build the firmware with

```
./build.sh -S bt
```

The provided `west.sh` script is a thin wrapper for Zephyr `west` command, to simplify handling.
For instance, to flash the board you can issue:

```
./west.sh flash
```

or maybe

```
./west.sh flash --no-rebuild --erase
```

Same goes for other `west` subcommands: for debugging, you would use

```
./west.sh debug
```

and so on.

# COPYING FILES #

Define `BASE` as current dir and `DEVICE` as the correct serial port:

```
BASE=`pwd`
DEVICE=/dev/ttyUSB0
```

To copy the base drivers to the Evernode:
```
$BASE/micropython/tools/mpremote/mpremote.py $DEVICE fs cp -r firmware/* :
```

To launch a test script on the Evernode:
```
$BASE/micropython/tools/mpremote/mpremote.py $DEVICE run tests/test_radio_async.py
```

If you get the error `ModuleNotFoundError: No module named 'serial'`, then install pyserial with

```
sudo apt install python3-pyserial
```

For a complete Micropython IDE, you can install Thonny:

```
sudo apt install pipx
pipx install thonny
```

and then simply launch it as

```
thonny
```

Clone this repo first:

```
git clone https://github.com/ant9000/evernode
cd evernode
```

Define `BASE` as current dir and `DEVICE` as the correct serial port:

```
BASE=`pwd`
DEVICE=/dev/ttyUSB0
```

Clone Micropython repo:

```
git clone --recurse-submodules https://github.com/micropython/micropython
```

Activate Zephyr environment and compile:

```
source ~/zephyrproject/.venv/bin/activate
./build.sh
```


For flashing the board:

```
./flash.sh
```

To copy the radio driver to the Evernode:
```
$BASE/micropython/tools/pyboard.py --device $DEVICE -f cp $BASE/sx1262.py :/flash/sx1262.py
```

To launch the radio test script on the Evernode:
```
$BASE/micropython/tools/pyboard.py --device $DEVICE $BASE/test_radio.py
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

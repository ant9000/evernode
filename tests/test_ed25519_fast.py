import ed25519_fast
import os, time

### needed to prime os.urandom()
import bluetooth
ble = bluetooth.BLE()
ble.active(True)
ble.active(False)
###

seed = os.urandom(32)
msg = b"test"

t = time.ticks_ms()
sig = ed25519_fast.sign(msg, seed)
print("sign:", time.ticks_diff(time.ticks_ms(), t), "ms")

pk = ed25519_fast.publickey(seed)
t = time.ticks_ms()
ok = ed25519_fast.verify(sig, msg, pk)
print("verify:", time.ticks_diff(time.ticks_ms(), t), "ms, ok:", ok)

t = time.ticks_ms()
pub = ed25519_fast.x25519_publickey(os.urandom(32))
print("x25519:", time.ticks_diff(time.ticks_ms(), t), "ms")

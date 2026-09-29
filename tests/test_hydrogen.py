import bluetooth
import hydrogen
import time

def test():
    TEST_CONTEXT = "EXAMPLES"
    TEST_DATA = "abcdefghijklmnopqrstuvwxyz"

    # bt_hci is used as entropy source; make sure BLE radio is on:
    ble = bluetooth.BLE()
    ble.active(True)

    hydrogen.init()

    s = time.time_ns()
    pub, pri = hydrogen.sign_keygen()
    e = time.time_ns()
    print("sign_keygen:", e-s)

    s = time.time_ns()
    signature = hydrogen.sign_create(TEST_CONTEXT, pri, TEST_DATA)
    e = time.time_ns()
    print("sign_create:", e-s)

    s = time.time_ns()
    verified = hydrogen.sign_verify(TEST_CONTEXT, pub, TEST_DATA, signature)
    e = time.time_ns()
    print("sign_verify:", e-s)

if __name__ == "__main__":
    test()


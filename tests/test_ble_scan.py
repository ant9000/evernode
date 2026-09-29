import asyncio, aioble, time

async def ble_scan():
    peers = {}
    async with aioble.scan(duration_ms=5000, interval_us=30000, window_us=30000, active=True) as scanner:
        async for result in scanner:
            peers[result.device.addr_hex()] = (result.name(), result.rssi)
    for addr in sorted(peers):
        name, rssi = peers[addr]
        print(addr, rssi, name)

aioble.device.ble.active(True)
asyncio.run(ble_scan())

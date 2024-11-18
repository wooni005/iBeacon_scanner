import asyncio
from bleak import BleakScanner
import struct

def parse_ibeacon(advertisement_data):
    # Check for iBeacon data
    manufacturer_data = advertisement_data.manufacturer_data
    if 0x4C in manufacturer_data:  # Apple company ID
        data = manufacturer_data[76]
        if data.startswith(b'\x02\x15'):  # iBeacon indicator
            uuid = data[2:18].hex()
            major, minor = struct.unpack('>HH', data[18:22])
            tx_power = struct.unpack('>b', data[22:23])[0]
            rssi = advertisement_data.rssi  # Received Signal Strength Indicator (RSSI)
            return uuid, major, minor, tx_power, rssi
    return None

async def scan_ibeacons():
    print("Scanning for iBeacons...")
    while True:
        try:
            async with BleakScanner(detection_callback=detection_callback) as scanner:
                await asyncio.sleep(10.0)
        except asyncio.CancelledError:
            print("Scanning stopped")
            break

async def detection_callback(device, advertisement_data):
    if device.address and advertisement_data:
        ibeacon_data = parse_ibeacon(advertisement_data)
        if ibeacon_data:
            uuid, major, minor, tx_power, rssi = ibeacon_data
            print("iBeacon Found!", end=' ')
            print(f"Device: {device.address}", end=' ')
            print(f"UUID: {uuid}", end=' ')
            print(f"Major: {major}", end=' ')
            print(f"Minor: {minor}", end=' ')
            print(f"TxPower: {tx_power}", end=' ')
            print("RSSI:", rssi)

if __name__ == "__main__":
    asyncio.run(scan_ibeacons())

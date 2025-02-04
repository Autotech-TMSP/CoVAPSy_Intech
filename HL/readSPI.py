import spidev #type: ignore #ignore the module could not be resolved error because it is a linux only module
import time
import struct

# Initialize SPI
spi = spidev.SpiDev()
spi.open(0, 0)  # Open SPI bus 0, device (CS) 0
spi.max_speed_hz = 50000

def read_voltage():
    # Send a dummy byte to initiate SPI communication
    response = spi.xfer2([0x00] * 8)  # 8 bytes to read two float values (4 bytes each)
    
    # Convert the received bytes to float values
    voltage_LiPo = struct.unpack('f', bytes(response[0:4]))[0]
    voltage_NiMh = struct.unpack('f', bytes(response[4:8]))[0]
    
    return voltage_LiPo, voltage_NiMh

try:
    while True:
        voltage_LiPo, voltage_NiMh = read_voltage()
        print(f"LiPo Voltage: {voltage_LiPo:.2f} V, NiMh Voltage: {voltage_NiMh:.2f} V")
        time.sleep(1)  # Adjust the delay as needed

except KeyboardInterrupt:
    spi.close()
    print("SPI communication closed.")
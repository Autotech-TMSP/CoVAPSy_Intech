import spidev #type: ignore #ignore the module could not be resolved error because it is a linux only module
import struct
import time

# Initialize SPI
spi = spidev.SpiDev()
spi.open(0, 0)  # Open SPI bus 0, device (CS) 0
spi.max_speed_hz = 50000

# Convert float to bytes
try:
    while True:
        send1 = 3.0
        send2 = 5.0
        send1_bytes = struct.pack('>f', send1)
        send2_bytes = struct.pack('>f', send2)

        # Send data to SPI slave
        # spi.xfer2([0x01])  # Send a dummy byte to initiate the transfer
        spi.xfer2(list(send1_bytes))
        spi.xfer2(list(send2_bytes))
        time.sleep(1)

        # Close SPI
    spi.close()
    
except FileNotFoundError:
    print("SPI device not found. Ensure SPI is enabled and the correct device file is used.")
except OSError as e:
    print(f"OS error: {e}")
except Exception as e:
    print(f"An error occurred: {e}")
import time
from luma.core.interface.serial import i2c
from luma.core.render import canvas
from luma.oled.device import ssd1306
from PIL import Image, ImageDraw, ImageFont
import struct
import smbus #type: ignore #ignore the module could not be resolved error because it is a linux only module

bus = smbus.SMBus(1)  # 1 indicates /dev/i2c-1

# I2C address of the slave
SLAVE_ADDRESS = 0x08
# I2C configuration
serial = i2c(port=1, address=0x3C)
device = ssd1306(serial)
font = ImageFont.load_default()

def write_data(data):
    # Convert string to list of ASCII values
    data_list = [ord(char) for char in data]
    bus.write_i2c_block_data(SLAVE_ADDRESS, 0, data_list)

def read_data(length):
    # Read a block of data from the slave
    data = bus.read_i2c_block_data(SLAVE_ADDRESS, 0, length)
    float1, float2 = struct.unpack('ff', data)
    return float1, float2




if __name__ == "__main__":
    try:

        # Request data from the slave
        received = read_data(2)  # Adjust length as needed
        print("Received from slave:", received)
        received_text = "LiPo: " + received[0] + "V    NiMh: " + received[1] + "V"
        with canvas(device) as draw:
            draw.text((0, 0), received, fill="white")

    except Exception as e:
        print("Error:", e)

while True:
    
    with canvas(device) as draw:
        draw.text((0, 0), "Hello World", fill="white")
    time.sleep(1)  # Adjust the delay as needed
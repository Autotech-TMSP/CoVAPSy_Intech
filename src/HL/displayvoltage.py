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
oled_display = ssd1306(serial)
font = ImageFont.load_default()

def write_data(data):
    # Convert string to list of ASCII values
    data_list = [ord(char) for char in data]
    bus.write_i2c_block_data(SLAVE_ADDRESS, 0, data_list)

def read_data(num_floats=3):
    
    # Each float is 4 bytes
    length = num_floats * 4
    # Read a block of data from the slave
    data = bus.read_i2c_block_data(SLAVE_ADDRESS, 0, length)
    # Convert the byte data to floats
    if len(data) >= length:
        float_values = struct.unpack('f' * num_floats, bytes(data[:length]))
        return list(float_values)
    else:
        raise ValueError("Not enough data received from I2C bus")
        
def displayvoltage():
        received = read_data(2)  # Adjust length as needed
        received= [ round(elem, 2) for elem in received ]
        for i in range(len(received)):
            if received[i] < 6:
                received[i] = 0.0
        # print(f"Received from slave: {received}")
        with canvas(oled_display) as draw:
            display_height = oled_display.height
            text = f"LiP:{received[0]:.2f}V|NiH:{received[1]:.2f}V"
            # _, text_height = draw.textsize(text, font=font) # Get the width and height of the text
            # text_height = draw.textlength(text, font=font, direction="ttb")
            text_height = 11
            print(f"Text height: {text_height}")
            text_y_position = display_height - text_height  # Position text at the bottom
            draw.text((0, text_y_position), text, fill="white", font=font)


if __name__ == "__main__":
    while True:
        displayvoltage()
    
import time
from luma.core.interface.serial import i2c
from luma.core.render import canvas
from luma.oled.device import ssd1306

from PIL import Image, ImageDraw, ImageFont, ImageSequence
# import smbus #type: ignore #ignore the module could not be resolved error because it is a linux only module
# bus = smbus.SMBus(1) # Create a new I2C bus

gif_path = "animation/improved_race_car_animation.gif"
gif = Image.open(gif_path)

# I2C configuration
serial = i2c(port=1, address=0x3C)
device = ssd1306(serial)

# Load default font.
font = ImageFont.load_default()

# Display "Hello World"
# with canvas(device) as draw:
#     text = "Hello World"
#     (draw_width, draw_height) = draw.textsize(text, font=font)
#     draw.text(((device.width - draw_width) / 2, (device.height - draw_height) / 2), text, font=font, fill=255)

# # Keep the display on for a while
# time.sleep(10)

while True:
    for frame in ImageSequence.Iterator(gif):
        with canvas(device) as draw:
            # Convert frame to RGB and resize to fit the device
            frame = frame.convert("RGB").resize((device.width, device.height))
            # Convert frame to 1-bit color
            frame = frame.convert("1")
            draw.bitmap((0, 0), frame, fill=1)
        time.sleep(0.1)  # Adjust the delay as needed

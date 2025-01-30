import time
from luma.core.interface.serial import i2c
from luma.core.render import canvas
from luma.oled.device import ssd1306
import Adafruit_SSD1306
# import gpiozero
from PIL import Image, ImageDraw, ImageFont
# import adafruit-circuitpython-ssd1306
# import smbus # import SMBus module of I2C
# bus = smbus.SMBus(1) # Create a new I2C bus

# I2C configuration
serial = i2c(port=1, address=0x3C)
device = ssd1306(serial)

# Load default font.
font = ImageFont.load_default()

# Display "Hello World"
with canvas(device) as draw:
    text = "Hello World"
    (draw_width, draw_height) = draw.textsize(text, font=font)
    draw.text(((device.width - draw_width) / 2, (device.height - draw_height) / 2), text, font=font, fill=255)

# Keep the display on for a while
time.sleep(10)
import time
from luma.core.interface.serial import i2c
from luma.core.render import canvas
from luma.oled.device import ssd1306
from PIL import Image, ImageDraw, ImageFont

# I2C configuration
serial = i2c(port=1, address=0x3C)
device = ssd1306(serial)

# Load default font.
font = ImageFont.load_default()



# Convert SVG to PNG
png_path = "animation/image.jpg"

# Open the PNG image
image = Image.open(png_path)

image = image.convert("1")
print(device.width, device.height)
while True:
    with canvas(device) as draw:
        draw.bitmap((0, 0), image, fill=1)
    time.sleep(0.1)  # Adjust the delay as needed

import time
import Adafruit_SSD1306
from PIL import Image, ImageDraw, ImageFont
import adafruit-circuitpython-ssd1306
import smbus # import SMBus module of I2C
bus = smbus.SMBus(1) # Create a new I2C bus

# Raspberry Pi pin configuration:
RST = None  # on the PiOLED this pin isn't used

platform = Platform.platform_detect()
if platform == Platform.RASPBERRY_PI:
    import Adafruit_GPIO.I2C as I2C
    I2C.require_repeated_start()

# 128x32 display with hardware I2C:
disp = Adafruit_SSD1306.SSD1306_128_32(rst=RST, i2c_address=0x3C)

# Initialize library.
disp.begin()

# Clear display.
disp.clear()
disp.display()

# Create blank image for drawing.
width = disp.width
height = disp.height
image = Image.new('1', (width, height))

# Get drawing object to draw on image.
draw = ImageDraw.Draw(image)

# Draw a black filled box to clear the image.
draw.rectangle((0, 0, width, height), outline=0, fill=0)

# Load default font.
font = ImageFont.load_default()

# Write "Hello World" on the display.
text = "Hello World"
(draw_width, draw_height) = draw.textsize(text, font=font)
draw.text(((width - draw_width) / 2, (height - draw_height) / 2), text, font=font, fill=255)

# Display image.
disp.image(image)
disp.display()
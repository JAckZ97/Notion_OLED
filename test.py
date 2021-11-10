import time
import Adafruit_GPIO.SPI as SPI
import Adafruit_SSD1306

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

import subprocess
import RPi.GPIO as GPIO
from datetime import datetime, timedelta

from RetriveDB import DatabaseController
from FetchFromJson import JsonFileController

# Raspberry Pi pin configuration:
RST = None     # on the PiOLED this pin isnt used
# Note the following are only used with SPI:
DC = 23
SPI_PORT = 0
SPI_DEVICE = 0

# 128x32 display with hardware I2C:
# disp = Adafruit_SSD1306.SSD1306_128_32(rst=RST)

# 128x64 display with hardware I2C:
disp = Adafruit_SSD1306.SSD1306_128_64(rst=RST)
# disp1 = Adafruit_SSD1306.SSD1306_128_64(rst=RST)

# Initialize library.
disp.begin()
# disp1.begin()

# Clear display.
disp.clear()
disp.display()
# disp1.clear()
# disp1.display()

# Create blank image for drawing.
# Make sure to create image with mode '1' for 1-bit color.
width = disp.width
height = disp.height
image = Image.new('1', (width, height))
# width1 = disp1.width
# height1 = disp1.height
# image1 = Image.new('1', (width1, height1))

# Get drawing object to draw on image.
draw = ImageDraw.Draw(image)
# draw1 = ImageDraw.Draw(image1)

# Draw a black filled box to clear the image.
draw.rectangle((0,0,width,height), outline=0, fill=0)
# draw1.rectangle((0,0,width1,height1), outline=0, fill=0)

# Draw some shapes.
# First define some constants to allow easy resizing of shapes.
padding = -2
top = padding
bottom = height-padding
# Move left to right keeping track of the current x position for drawing shapes.
x = 0

# Load default font.
font = ImageFont.load_default()
# Alternatively load a TTF font.  Make sure the .ttf font file is in the same directory as the python script!
# Some other nice fonts to try: http://www.dafont.com/bitmap.php
# font = ImageFont.truetype('Minecraftia.ttf', 8)

# setup GPIO pins
GPIO.setmode(GPIO.BCM)
GPIO.setup(5, GPIO.IN, pull_up_down = GPIO.PUD_UP)
GPIO.setup(16, GPIO.IN, pull_up_down = GPIO.PUD_UP)
GPIO.setup(17, GPIO.IN, pull_up_down = GPIO.PUD_UP)
GPIO.setup(26, GPIO.IN, pull_up_down = GPIO.PUD_UP)

counter = 0

while True:
    # Draw a black filled box to clear the image.
    draw.rectangle((0,0,width,height), outline=0, fill=0)
    # draw1.rectangle((0,0,width1,height1), outline=0, fill=0)

    # button for reset local database
    if GPIO.input(16) == False:
        counter += 1

    # button for confirming selections
    if GPIO.input(17) == False:
        while True:
            if GPIO.input(26) == False:
                break

            if GPIO.input(16) == False:
                counter += 1
                time.sleep(0.1)

            draw.text((x, top), 	str(counter), font = font, fill = 255)
            # Display image.
            disp.image(image)
            disp.display()
            time.sleep(0.1)

    # draw.text((x, top), 	str(counter), font = font, fill = 255)
    # # Display image.
    # disp.image(image)
    # disp.display()
    # time.sleep(.1)


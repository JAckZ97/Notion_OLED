import time
import Adafruit_GPIO.SPI as SPI
import Adafruit_SSD1306

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

import subprocess
import RPi.GPIO as GPIO
import time

from RetriveDB import DatabaseController
from FetchFromJson import JsonFileController

# Raspberry Pi pin configuration:
RST = None     # on the PiOLED this pin isnt used
# Note the following are only used with SPI:
DC = 23
SPI_PORT = 0
SPI_DEVICE = 0

# 128x32 display with hardware I2C:
disp = Adafruit_SSD1306.SSD1306_128_32(rst=RST)

# 128x64 display with hardware I2C:
# disp = Adafruit_SSD1306.SSD1306_128_64(rst=RST)

# Initialize library.
disp.begin()

# Clear display.
disp.clear()
disp.display()

# Create blank image for drawing.
# Make sure to create image with mode '1' for 1-bit color.
width = disp.width
height = disp.height
image = Image.new('1', (width, height))

# Get drawing object to draw on image.
draw = ImageDraw.Draw(image)

# Draw a black filled box to clear the image.
draw.rectangle((0,0,width,height), outline=0, fill=0)

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

# initialize dbcontroller and jsoncontroller
db = DatabaseController()
js = JsonFileController()


# while True:
# 	if GPIO.input(5) == False and GPIO.input(26) == False:
# 		print("Button_5 pressed")
# 		time.sleep(1)
# 	elif GPIO.input(16) == False:
# 		print("Reset Button pressed")
# 		time.sleep(1)	
# 	elif GPIO.input(17) == False:
# 		print("Button_1 pressed")
# 		time.sleep(1)

# 	elif GPIO.input(5) == False:
# 		print("Button_2 pressed")
# 		time.sleep(1)

# 	elif GPIO.input(26) == False:
# 		print("Button_3 pressed")
# 		time.sleep(1)

# 	else:
# 		continue

dayCount = 0
text_list = ["", "", "", ""]

while True:
    # Draw a black filled box to clear the image.
    draw.rectangle((0,0,width,height), outline=0, fill=0)

    # Write two lines of text.
    draw.text((x, top), 	text_list[0], font = font, fill = 255)
    draw.text((x, top+8),	text_list[1], font = font, fill = 255)
    draw.text((x, top+16),	text_list[2], font = font, fill = 255)
    draw.text((x, top+24),	text_list[3], font = font, fill = 255)

    if GPIO.input(5) == False:
        if dayCount == 5 or dayCount == 0:
            text_list[0] = js.getTodayDate()
            dayCount = 0
        elif dayCount == 1:
            text_list[0] = js.getYesterdayDate()
	        dayCount += 1
        elif dayCount == 2:
            text_list[0] = js.getTheDayBeforeYesterdayDate()
	        dayCount += 1
        elif dayCount == 3:
            text_list[0] = js.getTheDayAfterTmrDate()
	        dayCount += 1
        elif dayCount == 4:
            text_list[0] = js.getTmrDate()
	        dayCount += 1

        time.sleep(0.1)

    if GPIO.input(26) == False:
        text_list[0] = js.getYesterdayDate()        
	# dayCount += 1
        time.sleep(0.1)



    # Display image.
    disp.image(image)
    disp.display()
    time.sleep(.1)

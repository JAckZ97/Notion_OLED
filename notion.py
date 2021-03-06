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

# initialize dbcontroller and jsoncontroller
db = DatabaseController()
js = JsonFileController()


dayCount = 0
toggleCount = 0
toggleInsideCount = 0
# flag for sub task UI
subtask_flag = 0

text_list = ["", "", "", "", "", "", "", ""]
toggle_list = ["", "", "", "", "", ""]
toggle_inside_list = ["", "", "", "", "", ""]
content_list = ["", "", "", "", "", "", "", ""]
bracket_list = ["", "", "", "", "", ""]

# find the date today, yesterday, tomorrow, etc.
today = datetime.now()
yesterday = datetime.now() - timedelta(1)
the_day_before_yesterday = datetime.now() - timedelta(2)
tomorrow = datetime.now() + timedelta(1)
the_day_after_tomorrow = datetime.now() + timedelta(2)

today_str = datetime.strftime(today, '%Y-%m-%d')
yesterday_str = datetime.strftime(yesterday, '%Y-%m-%d')
the_day_before_yesterday_str = datetime.strftime(the_day_before_yesterday, '%Y-%m-%d')
tomorrow_str = datetime.strftime(tomorrow, '%Y-%m-%d')
the_day_after_tomorrow_str = datetime.strftime(the_day_after_tomorrow, '%Y-%m-%d')
temp_date_str = time.localtime()
# counter = 0

while True:
    # Draw a black filled box to clear the image.
    draw.rectangle((0,0,width,height), outline=0, fill=0)
    # draw1.rectangle((0,0,width1,height1), outline=0, fill=0)

    # reset local datebase if new day start
    if temp_date_str[:3] != time.localtime()[:3]:

        unfinished_task_list = []
        
        if dayCount == 1:
            page_list, children_list = js.getPageNameListWithChildrenStatus(today_str)
            time_str = js.getTodayDate()
        elif dayCount == 2:
            page_list, children_list = js.getPageNameListWithChildrenStatus(yesterday_str)
            time_str = js.getYesterdayDate()
        elif dayCount == 3:
            page_list, children_list = js.getPageNameListWithChildrenStatus(the_day_before_yesterday_str)
            time_str = js.getTheDayBeforeYesterdayDate()
        elif dayCount == 4:
            page_list, children_list = js.getPageNameListWithChildrenStatus(the_day_after_tomorrow_str)
            time_str = js.getTheDayAfterTmrDate()
        elif dayCount == 0:
            page_list, children_list = js.getPageNameListWithChildrenStatus(tomorrow_str)
            time_str = js.getTmrDate()
        else:
            continue

        try:
            if children_list[toggleCount] == False:
                continue
            # task has children
            elif children_list[toggleCount] == True:

                try:
                    # get the children list
                    task_list, task_id_list = js.getChildrenName(time_str, "TODO", True)

                    for item in range(0, len(task_list)):
                        if task_list[item][1] == True:
                            pass
                        elif task_list[item][1] == False:
                            unfinished_task_list.append(task_list[item][0])
                except:
                    continue
        except:
            continue

        # Create new TODO for tmr 
        db.createNewTODOforTmr(tomorrow_str,unfinished_task_list)
        # TODO: delet unfinished task of today????
        # ----------------------------------------

        # Write two lines of text.
        draw.text((x, top), 	"Resetting!", font = font, fill = 255)
        draw.text((x, top+9),	"", font = font, fill = 255)
        draw.text((x, top+17),	"", font = font, fill = 255)
        draw.text((x, top+25),	"", font = font, fill = 255)
        draw.text((x, top+33),	"", font = font, fill = 255)
        draw.text((x, top+41),	"", font = font, fill = 255)
        draw.text((x, top+49),	"", font = font, fill = 255)
        draw.text((x, top+57),	"", font = font, fill = 255)

        # Display image.
        disp.image(image)
        disp.display()
        time.sleep(0.1)

        db.readDatabase()
        time.sleep(0.1)
        js.resetBlockContent()
        time.sleep(0.1)
        # counter += 1
        # ----------------------------------------

    # button for reset local database
    if GPIO.input(16) == False:
        # Write two lines of text.
        draw.text((x, top), 	"Resetting!", font = font, fill = 255)
        draw.text((x, top+9),	"", font = font, fill = 255)
        draw.text((x, top+17),	"", font = font, fill = 255)
        draw.text((x, top+25),	"", font = font, fill = 255)
        draw.text((x, top+33),	"", font = font, fill = 255)
        draw.text((x, top+41),	"", font = font, fill = 255)
        draw.text((x, top+49),	"", font = font, fill = 255)
        draw.text((x, top+57),	"", font = font, fill = 255)

        # Display image.
        disp.image(image)
        disp.display()
        time.sleep(0.1)

        db.readDatabase()
        time.sleep(0.1)
        js.resetBlockContent()
        time.sleep(0.1)
        # counter += 1

    # button for confirming selections
    if GPIO.input(17) == False and subtask_flag == 0:
        if dayCount == 1:
            page_list, children_list = js.getPageNameListWithChildrenStatus(today_str)
            time_str = js.getTodayDate()
        elif dayCount == 2:
            page_list, children_list = js.getPageNameListWithChildrenStatus(yesterday_str)
            time_str = js.getYesterdayDate()
        elif dayCount == 3:
            page_list, children_list = js.getPageNameListWithChildrenStatus(the_day_before_yesterday_str)
            time_str = js.getTheDayBeforeYesterdayDate()
        elif dayCount == 4:
            page_list, children_list = js.getPageNameListWithChildrenStatus(the_day_after_tomorrow_str)
            time_str = js.getTheDayAfterTmrDate()
        elif dayCount == 0:
            page_list, children_list = js.getPageNameListWithChildrenStatus(tomorrow_str)
            time_str = js.getTmrDate()
        else:
            continue

        # if len(page_list) > 6:
        #     del page_list[6:len(page_list)]
        #     del children_list[6:len(children_list)]

        try:
            if children_list[toggleCount] == False:
                continue

            # task has children
            elif children_list[toggleCount] == True:
                subtask_flag = 1

                # update the newest information
                db.readDatabase()
                time.sleep(0.1)
                js.resetBlockContent()
                time.sleep(0.1)

                # get the children list
                task_list, task_id_list = js.getChildrenName(time_str, page_list[toggleCount], True)
                sub_task_status_list = [1, 1, 1, 1, 1, 1]
                content_list = ["", "", "", "", "", "", "", ""]
                bracket_list = ["", "", "", "", "", ""]

                for item in range(0, len(task_list)):
                    if task_list[item][1] == True:
                        bracket_list[item] = "[x]"
                        sub_task_status_list[item] = 1
                    elif task_list[item][1] == False:
                        bracket_list[item] = "[ ]"
                        sub_task_status_list[item] = 0
                    content_list[item+2] = task_list[item][0]

                # initial the toggle_inside
                toggle_inside_list[0] = "-> "
                toggle_inside_list[1] = "   "
                toggle_inside_list[2] = "   "
                toggle_inside_list[3] = "   "
                toggle_inside_list[4] = "   "
                toggle_inside_list[5] = "   "

                # get subtask title                  
                content_list[0] = page_list[toggleCount]

        except:
            continue
                
    # button for picking tasks by "->"
    if GPIO.input(5) == False and subtask_flag == 0:
        if dayCount == 1:
            page_list, children_list = js.getPageNameListWithChildrenStatus(today_str)
        elif dayCount == 2:
            page_list, children_list = js.getPageNameListWithChildrenStatus(yesterday_str)
        elif dayCount == 3:
            page_list, children_list = js.getPageNameListWithChildrenStatus(the_day_before_yesterday_str)
        elif dayCount == 4:
            page_list, children_list = js.getPageNameListWithChildrenStatus(the_day_after_tomorrow_str)
        elif dayCount == 0:
            page_list, children_list = js.getPageNameListWithChildrenStatus(tomorrow_str)
        else:
            continue

        if len(children_list) == 0:
            toggle_list[0] = "No task..."
            toggle_list[1] = ""
            toggle_list[2] = ""
            toggle_list[3] = ""
            toggle_list[4] = ""
            toggle_list[5] = ""
            
            if toggleCount >= len(page_list):
                toggleCount = 0
            time.sleep(0.1)
        
        elif toggleCount < len(page_list) and toggleCount == 0:
            toggle_list[0] = "   "
            toggle_list[1] = "-> "
            toggle_list[2] = "   "
            toggle_list[3] = "   "
            toggle_list[4] = "   "
            toggle_list[5] = "   "
            toggleCount += 1
            
            if toggleCount >= len(page_list):
                toggleCount = 0
                toggle_list = ["-> ", "   ", "   ", "   ", "   ", "   "]
            time.sleep(0.1)

        elif toggleCount < len(page_list) and toggleCount == 1:
            toggle_list[0] = "   "
            toggle_list[1] = "   "
            toggle_list[2] = "-> "
            toggle_list[3] = "   "
            toggle_list[4] = "   "
            toggle_list[5] = "   "
            toggleCount += 1

            if toggleCount >= len(page_list):
                toggleCount = 0
                toggle_list = ["-> ", "   ", "   ", "   ", "   ", "   "]
            time.sleep(0.1)

        elif toggleCount < len(page_list) and toggleCount == 2:
            toggle_list[0] = "   "
            toggle_list[1] = "   "
            toggle_list[2] = "   "
            toggle_list[3] = "-> "
            toggle_list[4] = "   "
            toggle_list[5] = "   "
            toggleCount += 1

            if toggleCount >= len(page_list):
                toggleCount = 0
                toggle_list = ["-> ", "   ", "   ", "   ", "   ", "   "]
            time.sleep(0.1)

        elif toggleCount < len(page_list) and toggleCount == 3:
            toggle_list[0] = "   "
            toggle_list[1] = "   "
            toggle_list[2] = "   "
            toggle_list[3] = "   "
            toggle_list[4] = "-> "
            toggle_list[5] = "   "
            toggleCount += 1

            if toggleCount >= len(page_list):
                toggleCount = 0
                toggle_list = ["-> ", "   ", "   ", "   ", "   ", "   "]
            time.sleep(0.1)

        elif toggleCount < len(page_list) and toggleCount == 4:
            toggle_list[0] = "   "
            toggle_list[1] = "   "
            toggle_list[2] = "   "
            toggle_list[3] = "   "
            toggle_list[4] = "   "
            toggle_list[5] = "-> "
            toggleCount += 1

            if toggleCount >= len(page_list):
                toggleCount = 0
                toggle_list = ["-> ", "   ", "   ", "   ", "   ", "   "]
            time.sleep(0.1)

        elif toggleCount < len(page_list) and toggleCount == 5:
            toggle_list[0] = "-> "
            toggle_list[1] = "   "
            toggle_list[2] = "   "
            toggle_list[3] = "   "
            toggle_list[4] = "   "
            toggle_list[5] = "   "
            toggleCount = 0
            time.sleep(0.1)

        elif toggleCount >= len(page_list):
            toggle_list[0] = "-> "
            toggle_list[1] = "   "
            toggle_list[2] = "   "
            toggle_list[3] = "   "
            toggle_list[4] = "   "
            toggle_list[5] = "   "
            toggleCount = 0
            time.sleep(0.1)
        else:
            continue

    # button for switching days
    if GPIO.input(26) == False and subtask_flag == 0:
        if dayCount == 0:
            text_list[0] = js.getTodayDate()
            page_list, children_list = js.getPageNameListWithChildrenStatus(today_str)
            for num in range(0, len(page_list)):
                text_list[num+2] = page_list[num]
            
            for empty in range(len(page_list), 6):
                text_list[empty+2] = ""
            dayCount += 1
            toggleCount = 0
            if len(children_list) == 0:
                toggle_list[0] = "No task..."
                toggle_list[1] = ""
                toggle_list[2] = ""
                toggle_list[3] = ""
                toggle_list[4] = ""
                toggle_list[5] = ""
            else:
                toggle_list[0] = "-> "
                toggle_list[1] = "   "
                toggle_list[2] = "   "
                toggle_list[3] = "   "
                toggle_list[4] = "   "
                toggle_list[5] = "   "
            time.sleep(0.1)

        elif dayCount == 1:
            text_list[0] = js.getYesterdayDate()
            page_list, children_list = js.getPageNameListWithChildrenStatus(yesterday_str)
            for num in range(0, len(page_list)):
                text_list[num+2] = page_list[num]
            
            for empty in range(len(page_list), 6):
                text_list[empty+2] = ""
            dayCount += 1
            toggleCount = 0
            if len(children_list) == 0:
                toggle_list[0] = "No task..."
                toggle_list[1] = ""
                toggle_list[2] = ""
                toggle_list[3] = ""
                toggle_list[4] = ""
                toggle_list[5] = ""
            else:
                toggle_list[0] = "-> "
                toggle_list[1] = "   "
                toggle_list[2] = "   "
                toggle_list[3] = "   "
                toggle_list[4] = "   "
                toggle_list[5] = "   "
            time.sleep(0.1)

        elif dayCount == 2:
            text_list[0] = js.getTheDayBeforeYesterdayDate()
            page_list, children_list = js.getPageNameListWithChildrenStatus(the_day_before_yesterday_str)
            for num in range(0, len(page_list)):
                text_list[num+2] = page_list[num]
            
            for empty in range(len(page_list), 6):
                text_list[empty+2] = ""
            dayCount += 1
            toggleCount = 0
            if len(children_list) == 0:
                toggle_list[0] = "No task..."
                toggle_list[1] = ""
                toggle_list[2] = ""
                toggle_list[3] = ""
                toggle_list[4] = ""
                toggle_list[5] = ""
            else:
                toggle_list[0] = "-> "
                toggle_list[1] = "   "
                toggle_list[2] = "   "
                toggle_list[3] = "   "
                toggle_list[4] = "   "
                toggle_list[5] = "   "
            time.sleep(0.1)

        elif dayCount == 3:
            text_list[0] = js.getTheDayAfterTmrDate()
            page_list, children_list = js.getPageNameListWithChildrenStatus(the_day_after_tomorrow_str)
            for num in range(0, len(page_list)):
                text_list[num+2] = page_list[num]
            
            for empty in range(len(page_list), 6):
                text_list[empty+2] = ""
            dayCount += 1
            toggleCount = 0
            if len(children_list) == 0:
                toggle_list[0] = "No task..."
                toggle_list[1] = ""
                toggle_list[2] = ""
                toggle_list[3] = ""
                toggle_list[4] = ""
                toggle_list[5] = ""
            else:
                toggle_list[0] = "-> "
                toggle_list[1] = "   "
                toggle_list[2] = "   "
                toggle_list[3] = "   "
                toggle_list[4] = "   "
                toggle_list[5] = "   "
            time.sleep(0.1)

        elif dayCount == 4:
            text_list[0] = js.getTmrDate()
            page_list, children_list = js.getPageNameListWithChildrenStatus(tomorrow_str)
            for num in range(0, len(page_list)):
                text_list[num+2] = page_list[num]
            
            for empty in range(len(page_list), 6):
                text_list[empty+2] = ""
            dayCount = 0
            toggleCount = 0
            if len(children_list) == 0:
                toggle_list[0] = "No task..."
                toggle_list[1] = ""
                toggle_list[2] = ""
                toggle_list[3] = ""
                toggle_list[4] = ""
                toggle_list[5] = ""
            else:
                toggle_list[0] = "-> "
                toggle_list[1] = "   "
                toggle_list[2] = "   "
                toggle_list[3] = "   "
                toggle_list[4] = "   "
                toggle_list[5] = "   "
            time.sleep(0.1)
        else:
            continue

    # button for confirming selections
    if GPIO.input(17) == False and subtask_flag == 1:
        if sub_task_status_list[toggleInsideCount] == 1:
            bracket_list[toggleInsideCount] = "[ ]"
            sub_task_status_list[toggleInsideCount] = 0
        elif sub_task_status_list[toggleInsideCount] == 0:
            bracket_list[toggleInsideCount] = "[x]"
            sub_task_status_list[toggleInsideCount] = 1
            
        js.updateTodoSubtask(task_id_list[toggleInsideCount])
    
    # button for picking subtasks by "->"
    if GPIO.input(5) == False and subtask_flag == 1:
        if toggleInsideCount < len(task_list) and toggleInsideCount == 0:
            toggle_inside_list[0] = "   "
            toggle_inside_list[1] = "-> "
            toggle_inside_list[2] = "   "
            toggle_inside_list[3] = "   "
            toggle_inside_list[4] = "   "
            toggle_inside_list[5] = "   "
            toggleInsideCount += 1
            
            if toggleInsideCount >= len(task_list):
                toggleInsideCount = 0
                toggle_inside_list = ["-> ", "   ", "   ", "   ", "   ", "   "]
            time.sleep(0.1)

        elif toggleInsideCount < len(task_list) and toggleInsideCount == 1:
            toggle_inside_list[0] = "   "
            toggle_inside_list[1] = "   "
            toggle_inside_list[2] = "-> "
            toggle_inside_list[3] = "   "
            toggle_inside_list[4] = "   "
            toggle_inside_list[5] = "   "
            toggleInsideCount += 1
            
            if toggleInsideCount >= len(task_list):
                toggleInsideCount = 0
                toggle_inside_list = ["-> ", "   ", "   ", "   ", "   ", "   "]
            time.sleep(0.1)

        elif toggleInsideCount < len(task_list) and toggleInsideCount == 2:
            toggle_inside_list[0] = "   "
            toggle_inside_list[1] = "   "
            toggle_inside_list[2] = "   "
            toggle_inside_list[3] = "-> "
            toggle_inside_list[4] = "   "
            toggle_inside_list[5] = "   "
            toggleInsideCount += 1
            
            if toggleInsideCount >= len(task_list):
                toggleInsideCount = 0
                toggle_inside_list = ["-> ", "   ", "   ", "   ", "   ", "   "]
            time.sleep(0.1)

        elif toggleInsideCount < len(task_list) and toggleInsideCount == 3:
            toggle_inside_list[0] = "   "
            toggle_inside_list[1] = "   "
            toggle_inside_list[2] = "   "
            toggle_inside_list[3] = "   "
            toggle_inside_list[4] = "-> "
            toggle_inside_list[5] = "   "
            toggleInsideCount += 1
            
            if toggleInsideCount >= len(task_list):
                toggleInsideCount = 0
                toggle_inside_list = ["-> ", "   ", "   ", "   ", "   ", "   "]
            time.sleep(0.1)

        elif toggleInsideCount < len(task_list) and toggleInsideCount == 4:
            toggle_inside_list[0] = "   "
            toggle_inside_list[1] = "   "
            toggle_inside_list[2] = "   "
            toggle_inside_list[3] = "   "
            toggle_inside_list[4] = "   "
            toggle_inside_list[5] = "-> "
            toggleInsideCount += 1
            
            if toggleInsideCount >= len(task_list):
                toggleInsideCount = 0
                toggle_inside_list = ["-> ", "   ", "   ", "   ", "   ", "   "]
            time.sleep(0.1)

        elif toggleInsideCount < len(task_list) and toggleInsideCount == 5:
            toggle_inside_list[0] = "-> "
            toggle_inside_list[1] = "   "
            toggle_inside_list[2] = "   "
            toggle_inside_list[3] = "   "
            toggle_inside_list[4] = "   "
            toggle_inside_list[5] = "   "
            toggleInsideCount += 1
            
            if toggleInsideCount >= len(task_list):
                toggleInsideCount = 0
                toggle_inside_list = ["-> ", "   ", "   ", "   ", "   ", "   "]
            time.sleep(0.1)
    
        elif toggleInsideCount >= len(task_list):
            toggle_inside_list[0] = "-> "
            toggle_inside_list[1] = "   "
            toggle_inside_list[2] = "   "
            toggle_inside_list[3] = "   "
            toggle_inside_list[4] = "   "
            toggle_inside_list[5] = "   "
            toggleInsideCount = 0
            time.sleep(0.1)
        else:
            continue

    # button for leave sub-task page 
    if GPIO.input(26) == False and subtask_flag == 1:
        toggleInsideCount = 0
        subtask_flag = 0

    # for testing purpose
    if GPIO.input(16) == False and subtask_flag == 1:
        unfinished_task_list = []
        
        if dayCount == 1:
            page_list, children_list = js.getPageNameListWithChildrenStatus(today_str)
            time_str = js.getTodayDate()
        elif dayCount == 2:
            page_list, children_list = js.getPageNameListWithChildrenStatus(yesterday_str)
            time_str = js.getYesterdayDate()
        elif dayCount == 3:
            page_list, children_list = js.getPageNameListWithChildrenStatus(the_day_before_yesterday_str)
            time_str = js.getTheDayBeforeYesterdayDate()
        elif dayCount == 4:
            page_list, children_list = js.getPageNameListWithChildrenStatus(the_day_after_tomorrow_str)
            time_str = js.getTheDayAfterTmrDate()
        elif dayCount == 0:
            page_list, children_list = js.getPageNameListWithChildrenStatus(tomorrow_str)
            time_str = js.getTmrDate()
        else:
            continue

        try:
            if children_list[toggleCount] == False:
                continue
            # task has children
            elif children_list[toggleCount] == True:

                try:
                    # get the children list
                    task_list, task_id_list = js.getChildrenName(time_str, "TODO", True)

                    for item in range(0, len(task_list)):
                        if task_list[item][1] == True:
                            pass
                        elif task_list[item][1] == False:
                            unfinished_task_list.append(task_list[item][0])
                except:
                    continue
        except:
            continue

        # Create new TODO for tmr 
        db.createNewTODOforTmr(tomorrow_str,unfinished_task_list)
        
    if subtask_flag == 0:
        # Write two lines of text.
        draw.text((x, top), 	text_list[0], font = font, fill = 255)
        draw.text((x, top+9),	text_list[1], font = font, fill = 255)
        draw.text((x, top+17),	toggle_list[0] + text_list[2], font = font, fill = 255)
        draw.text((x, top+25),	toggle_list[1] + text_list[3], font = font, fill = 255)
        draw.text((x, top+33),	toggle_list[2] + text_list[4], font = font, fill = 255)
        draw.text((x, top+41),	toggle_list[3] + text_list[5], font = font, fill = 255)
        draw.text((x, top+49),	toggle_list[4] + text_list[6], font = font, fill = 255)
        draw.text((x, top+57),	toggle_list[5] + text_list[7], font = font, fill = 255)
        # draw.text((x, top), 	str(counter), font = font, fill = 255)

        # Display image.
        disp.image(image)
        disp.display()
        time.sleep(.1)
    
    elif subtask_flag == 1:
        # Write two lines of text.
        draw.text((x, top), 	content_list[0], font = font, fill = 255)
        draw.text((x, top+9),	content_list[1], font = font, fill = 255)
        draw.text((x, top+17),	toggle_inside_list[0] + bracket_list[0] + content_list[2], font = font, fill = 255)
        draw.text((x, top+25),	toggle_inside_list[1] + bracket_list[1] + content_list[3], font = font, fill = 255)
        draw.text((x, top+33),	toggle_inside_list[2] + bracket_list[2] + content_list[4], font = font, fill = 255)
        draw.text((x, top+41),	toggle_inside_list[3] + bracket_list[3] + content_list[5], font = font, fill = 255)
        draw.text((x, top+49),	toggle_inside_list[4] + bracket_list[4] + content_list[6], font = font, fill = 255)
        draw.text((x, top+57),	toggle_inside_list[5] + bracket_list[5] + content_list[7], font = font, fill = 255)

        # Display image.
        disp.image(image)
        disp.display()
        time.sleep(0.1)

    else:
        continue


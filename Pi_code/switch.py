import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)

GPIO.setup(17, GPIO.IN, pull_up_down = GPIO.PUD_UP)
GPIO.setup(5, GPIO.IN, pull_up_down = GPIO.PUD_UP)
GPIO.setup(26, GPIO.IN, pull_up_down = GPIO.PUD_UP)
GPIO.setup(16, GPIO.IN, pull_up_down = GPIO.PUD_UP)

while True:

	if GPIO.input(5) == False and GPIO.input(26) == False:
		print("Button_5 pressed")
		time.sleep(1)
	elif GPIO.input(16) == False:
		print("Reset Button pressed")
		time.sleep(1)	
	elif GPIO.input(17) == False:
		print("Button_1 pressed")
		time.sleep(1)

	elif GPIO.input(5) == False:
		print("Button_2 pressed")
		time.sleep(1)

	elif GPIO.input(26) == False:
		print("Button_3 pressed")
		time.sleep(1)

	else:
		continue

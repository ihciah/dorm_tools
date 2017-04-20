#!/usr/bin/python
import RPi.GPIO as GPIO
import time
door_pin = 18
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(door_pin, GPIO.OUT)
GPIO.output(door_pin, True)
time.sleep(1)
GPIO.output(door_pin, False)

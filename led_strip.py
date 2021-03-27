import RPi.GPIO as GPIO
from time import sleep

led_strip_pin = 21

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

GPIO.setup(led_strip_pin, GPIO.OUT, initial=GPIO.LOW)

for i in range(10):
    print('HIGH')
    GPIO.output(led_strip_pin, GPIO.HIGH) 
    sleep(1)

    print('LOW')
    GPIO.output(led_strip_pin, GPIO.LOW)
    sleep(1)


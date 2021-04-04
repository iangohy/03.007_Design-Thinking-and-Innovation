import RPi.GPIO as GPIO
from time import sleep
import logging

class Led_strip:
    def __init__(self, pin):
        self.pin = pin
        GPIO.setup(pin, GPIO.OUT, initial=GPIO.LOW)

    def blink(self, duration=15):
        total_count = int(duration / 3)

        for i in range(total_count):
            logging.info("HIGH")
            GPIO.output(self.pin, GPIO.HIGH)
            sleep(2)

            logging.info("LOW")
            GPIO.output(self.pin, GPIO.LOW)
            sleep(1)

        GPIO.output(self.pin, GPIO.LOW)

def setup():
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)

if __name__ == "__main__":
    format = "%(asctime)s: %(message)s"
    logging.basicConfig(format=format, level=logging.INFO,
                        datefmt="%H:%M:%S")
    setup()

    white_led = Led_strip(21)
    white_led.blink()

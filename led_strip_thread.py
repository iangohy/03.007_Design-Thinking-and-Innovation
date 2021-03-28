import RPi.GPIO as GPIO
from time import sleep
import logging
import threading

class LedThread(threading.Thread):
    def __init__(self, pin, duration):
        threading.Thread.__init__(self)
        self.pin = pin
        self.duration = duration
        GPIO.setup(pin, GPIO.OUT, initial=GPIO.LOW)

    def run(self):
        total_count = int(self.duration / 3)
        
        GPIO.output(self.pin, GPIO.HIGH)
        sleep(1)

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

    white_led_thread = LedThread(21, 15)
    white_led_thread.start()
    print("hello world!")

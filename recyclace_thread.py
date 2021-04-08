import lib.barcode as barcode
import lib.stepper as stepper

import csv
from time import sleep
import logging
import threading
import os
import RPi.GPIO as GPIO

PLASTIC_PIN = 16
PAPER_PIN = 26
CAN_PIN = 21
WASTE_PIN = 20

BLINK_COUNT = 2

LED_COUNTER = {"plastic": 1, "paper": 1, "can": 1, "waste": 1}

class LedThread(threading.Thread):
    def __init__(self, pin, category):
        threading.Thread.__init__(self, daemon=True)
        self.pin = pin
        self.category = category
        GPIO.setup(pin, GPIO.OUT, initial=GPIO.LOW)

    def run(self):
        global LED_COUNTER
        while True:
            # Check condition
            if LED_COUNTER[self.category] > 0:
                logging.info(self.category + " HIGH")
                GPIO.output(self.pin, GPIO.HIGH)
                sleep(5)

                logging.info(self.category + " LOW")
                GPIO.output(self.pin, GPIO.LOW)
                sleep(0.5)

                LED_COUNTER[self.category] -= 1
            else:
                GPIO.output(self.pin, GPIO.LOW)

            # Wait
            sleep(1)

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

def classifyWaste():
    while True:
        category = barcode.getBarcodeData()
        LED_COUNTER[category] = BLINK_COUNT

def setup():
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)

if __name__ == "__main__":
    format = "%(asctime)s: %(message)s"
    logging.basicConfig(format=format, level=logging.INFO,
                        datefmt="%H:%M:%S")
    logging.info("Recyclace software started!")
    setup()
    
    can_led_thread = LedThread(CAN_PIN, "can")
    can_led_thread.start()

    waste_led_thread = LedThread(WASTE_PIN, "waste")
    waste_led_thread.start()

    paper_led_thread = LedThread(PAPER_PIN, "paper")
    paper_led_thread.start()

    plastic_led_thread = LedThread(PLASTIC_PIN, "plastic")
    plastic_led_thread.start()
    
    barcodeThread = threading.Thread(target=classifyWaste)
    barcodeThread.start()
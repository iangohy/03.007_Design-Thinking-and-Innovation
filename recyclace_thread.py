import lib.barcode as barcode
import lib.stepper as stepper

import csv
from time import sleep
import logging
import threading
import os
import RPi.GPIO as GPIO

PLASTIC_PIN = 16    # RED
PAPER_PIN = 26  # BLUE
CAN_PIN = 19    # YELLOW
WASTE_PIN = 20  # GREEN
BUTTON_PIN = 14
ENA_PIN = 17
DIR_PIN = 27
PUL_PIN = 22
RPS = 1
PULSE_PER_REV = 800
PERECENT_PER_REV = 10

BLINK_COUNT = 4

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
                sleep(1.5)

                logging.info(self.category + " LOW")
                GPIO.output(self.pin, GPIO.LOW)
                sleep(0.2)

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

def classifyWasteTesting():
    while True:
        category = input("[TESTING MODE] Manually input category:")
        LED_COUNTER[category] = BLINK_COUNT

def moveMotorButtonPress():
    while True:
        if GPIO.input(BUTTON_PIN):
            logging.info("Button press!")
            motor_1 = stepper.StepperMotor(enablePin=ENA_PIN, dirPin=DIR_PIN, pulsePin=PUL_PIN, rps = RPS, pulsePerRev = PULSE_PER_REV, percentPerRev=PERCENT_PER_REV)
            motor_1.rotate(3)
            motor_1.rotate(-3)
            sleep(5)

def setup():
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)

    GPIO.setup(BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

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
    
    if os.getenv('recyclace') == "testing":
        barcodeThread = threading.Thread(target=classifyWasteTesting)
    else:
        barcodeThread = threading.Thread(target=classifyWaste)
    barcodeThread.start()

    motorThread = threading.Thread(target=moveMotorButtonPress, daemon=True)
    motorThread.start()

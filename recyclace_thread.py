import csv
import RPi.GPIO as GPIO
from time import sleep
import logging
import threading

PLASTIC_PIN = 16
PAPER_PIN = 26
CAN_PIN = 21
WASTE_PIN = 20

BLINK_COUNT = 3

LED_COUNTER = {"plastic": 0, "paper": 0, "can": 0, "waste": 0}

hid = { 4: 'a', 5: 'b', 6: 'c', 7: 'd', 8: 'e', 9: 'f', 10: 'g', 11: 'h', 12: 'i', 13: 'j', 14: 'k', 15: 'l', 16: 'm', 17: 'n', 18: 'o', 19: 'p', 20: 'q', 21: 'r', 22: 's', 23: 't', 24: 'u', 25: 'v', 26: 'w', 27: 'x', 28: 'y', 29: 'z', 30: '1', 31: '2', 32: '3', 33: '4', 34: '5', 35: '6', 36: '7', 37: '8', 38: '9', 39: '0', 44: ' ', 45: '-', 46: '=', 47: '[', 48: ']', 49: '\\', 51: ';' , 52: '\'', 53: '~', 54: ',', 55: '.', 56: '/'  }

hid2 = { 4: 'A', 5: 'B', 6: 'C', 7: 'D', 8: 'E', 9: 'F', 10: 'G', 11: 'H', 12: 'I', 13: 'J', 14: 'K', 15: 'L', 16: 'M', 17: 'N', 18: 'O', 19: 'P', 20: 'Q', 21: 'R', 22: 'S', 23: 'T', 24: 'U', 25: 'V', 26: 'W', 27: 'X', 28: 'Y', 29: 'Z', 30: '!', 31: '@', 32: '#', 33: '$', 34: '%', 35: '^', 36: '&', 37: '*', 38: '(', 39: ')', 44: ' ', 45: '_', 46: '+', 47: '{', 48: '}', 49: '|', 51: ':' , 52: '"', 53: '~', 54: '<', 55: '>', 56: '?'  }

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
                sleep(2)

                logging.info(self.category + " LOW")
                GPIO.output(self.pin, GPIO.LOW)
                sleep(1)

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

def readBarcode():
    try:
        fp = open('/dev/hidraw0', 'rb')

        res = ""
        while True:
            # Read barcode scan
            buffer = fp.read(8)
            shift = False
            for c in buffer:
                if c > 0:
                    if c == 2:
                        shift = True
                        continue
                    if shift == True:
                        res += hid2[int(c)]
                    else:
                        if c == 40:
                            logging.info("Barcode scanned: " + res)
                            return(res)    
                        else:
                            res += hid[int(c)]
    except FileNotFoundError:
        logging.error("[ERROR] Unable to connect to barcode scanner! Is it plugged in?")
        logging.info("Recyclace software quitting...")
        quit()
    except:
        print("Unexpected error:", sys.exc_info()[0])
        raise

def getBarcodeData():
    res = readBarcode() 
    # Check against database
    with open("data.csv") as data:
        reader = csv.reader(data)
        item = []
        for row in reader:
            if row[0] == res:
                item = row
                logging.info(f">>> name: {item[1]} | type: {item[2]} | barcode: {item[0]}")
                return item[2]
        if not item:
            logging.info(f"Barcode {res} not found! Classifying as waste")
            return "waste"

def classifyWaste():
    while True:
        category = getBarcodeData()
        print(category)
        LED_COUNTER[category] += BLINK_COUNT

def setup():
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)

if __name__ == "__main__":
    format = "%(asctime)s: %(message)s"
    logging.basicConfig(format=format, level=logging.INFO,
                        datefmt="%H:%M:%S")
    logging.info("Recyclace software started!")
    setup()
    
    barcodeThread = threading.Thread(target=classifyWaste)
    barcodeThread.start()

    can_led_thread = LedThread(CAN_PIN, "can")
    can_led_thread.start()

    waste_led_thread = LedThread(WASTE_PIN, "waste")
    waste_led_thread.start()


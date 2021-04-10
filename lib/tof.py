# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT
 
# Simple demo of the VL53L0X distance sensor.
# Will print the sensed range/distance every second.
import time
 
import board
import busio
 
import adafruit_vl53l0x

def setup():
    # Initialize I2C bus and sensor.
    i2c = busio.I2C(board.SCL, board.SDA)
    vl53 = adafruit_vl53l0x.VL53L0X(i2c)

def getDistance():
    try:
        setup()
        while True:
            # Optionally adjust the measurement timing budget to change speed and accuracy.
            # See the example here for more details:
            #   https://github.com/pololu/vl53l0x-arduino/blob/master/examples/Single/Single.ino
            # For example a higher speed but less accurate timing budget of 20ms:
            # vl53.measurement_timing_budget = 20000
            # Or a slower but more accurate timing budget of 200ms:
            # vl53.measurement_timing_budget = 200000
            # The default timing budget is 33ms, a good compromise of speed and accuracy.
            distance = vl53.range
            return distance
    except:
        return -1

def main():
    format = "%(asctime)s: %(message)s"
    logging.basicConfig(format=format, level=logging.INFO,
                        datefmt="%H:%M:%S")
    logging.info("Recyclace software started!")

    try:
        while True:
            distance = getDistance()
            print(f"Distance from sensor 1: {distance}")
            time.sleep(2)
    except:
        logging.info("Unable to read I2C, is sensor connected?")
        return


if __name__ == "__main__":
    main()
 

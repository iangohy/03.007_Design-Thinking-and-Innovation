# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT
 
# Simple demo of the VL53L0X distance sensor.
# Will print the sensed range/distance every second.
import time
import logging
 
import board
import busio
 
import adafruit_vl53l0x

def getDistance(interval, maxHeight):
 
    # Initialize I2C bus and sensor.
    i2c = busio.I2C(board.SCL, board.SDA)
    vl53 = adafruit_vl53l0x.VL53L0X(i2c)
    
    # Optionally adjust the measurement timing budget to change speed and accuracy.
    # See the example here for more details:
    #   https://github.com/pololu/vl53l0x-arduino/blob/master/examples/Single/Single.ino
    # For example a higher speed but less accurate timing budget of 20ms:
    # vl53.measurement_timing_budget = 20000
    # Or a slower but more accurate timing budget of 200ms:
    # vl53.measurement_timing_budget = 200000
    # The default timing budget is 33ms, a good compromise of speed and accuracy.
    
    # Main loop will read the range and print it every second.
    while True:
        dist = vl53.range / 10
        percentage = (maxHeight - dist) / maxHeight * 100
        if percentage > 95:
            percentage = 100
        elif percentage < 0:
            percentage = 0
        logging.info(f">>>>>>>Distance Measured: {dist}cm, {percentage}% filled")
        time.sleep(interval)

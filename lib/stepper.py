from time import sleep
import RPi.GPIO as GPIO

class StepperMotor:
    def __init__(self, enable_pin=17, dir_pin=27, pulse_pin=22, rps = 1, pulse_per_rev = 800, percent_per_rev = 10):
        self.enable_pin = enable_pin
        self.dir_pin = dir_pin
        self.pulse_pin = pulse_pin
        self.rps = rps
        self.pulse_per_rev = pulse_per_rev
        self.percent_per_rev = percent_per_rev
        with open("stepper_loc.txt", "r") as location:
            self.percent = location.read()
            print(f"Stepper currently at {self.percent}%")


        GPIO.setmode(GPIO.BCM)
        GPIO.setup(dir_pin, GPIO.OUT)
        GPIO.setup(enable_pin, GPIO.OUT)
        GPIO.setup(pulse_pin, GPIO.OUT)
        GPIO.setwarnings(False)

        GPIO.output(enable_pin, GPIO.HIGH)

    def rotate(self, num_rev = 1):
        # Set direction
        if num_rev >= 0:
            direction = "clockwise"
            GPIO.output(self.dir_pin, GPIO.HIGH)
        else:
            direction = "anti-clockwise"
            num_rev = -num_rev
            GPIO.output(self.dir_pin, GPIO.LOW)

        print(f"Rotating {num_rev} revolution(s) {direction} at {self.rps} revolutions per second")
        for i in range(self.pulse_per_rev * num_rev):
            sleep_len = 1/(2 * self.pulse_per_rev * self.rps)
            # sleep_len = 0.01

            GPIO.output(self.pulse_pin, GPIO.HIGH)
            # print("-")
            sleep(sleep_len)
            GPIO.output(self.pulse_pin, GPIO.LOW)
            # print(".")
            sleep(sleep_len)

        self.percent += num_rev * self.percent_per_rev
        print(f"Stepper now at {self.percent}%")

        with open("stepper_loc.txt", "w") as location:
            location.write(self.percent)

def main():
    nema23 = StepperMotor(rps = 1, pulse_per_rev = 1600)
    nema23.rotate(3)
    nema23.rotate(-3)

if __name__ == "__main__":
    main()

from time import sleep
import RPi.GPIO as GPIO

class StepperMotor:
    def __init__(self, enablePin=17, dirPin=27, pulsePin=22, \
        rps = 1, pulsePerRev = 800, percentPerRev = 10, \
            percentMax=80, percentMin=20):

        self.enablePin = enablePin
        self.dirPin = dirPin
        self.pulsePin = pulsePin
        self.rps = rps
        self.pulsePerRev = pulsePerRev
        self.percentPerRev = percentPerRev
        self.percentMax = percentMax
        self.percentMin = percentMin
        with open("stepper_loc.txt", "r") as location:
            self.percent = int(location.read())
            print(f"Stepper currently at {self.percent}%")


        GPIO.setmode(GPIO.BCM)
        GPIO.setup(dirPin, GPIO.OUT)
        GPIO.setup(enablePin, GPIO.OUT)
        GPIO.setup(pulsePin, GPIO.OUT)
        GPIO.setwarnings(False)

        GPIO.output(enablePin, GPIO.HIGH)

    def rotate(self, num_rev = 1):
        # Set direction
        if num_rev >= 0:
            direction = "clockwise"
            GPIO.output(self.dirPin, GPIO.HIGH)
        else:
            direction = "anti-clockwise"
            num_rev = -num_rev
            GPIO.output(self.dirPin, GPIO.LOW)

        print(f"Rotating {num_rev} revolution(s) {direction} at {self.rps} revolutions per second")
        for i in range(int(self.pulsePerRev * num_rev)):
            sleep_len = 1/(2 * self.pulsePerRev * self.rps)
            # sleep_len = 0.01

            GPIO.output(self.pulsePin, GPIO.HIGH)
            # print("-")
            sleep(sleep_len)
            GPIO.output(self.pulsePin, GPIO.LOW)
            # print(".")
            sleep(sleep_len)

        print(f"Stepper now at {self.percent}%")

        with open("stepper_loc.txt", "w") as location:
            location.write(f"{self.percent}")

    def rotateTo(self, percent):
        currentPercent = self.percent
        percentMax = self.percentMax
        percentMin = self.percentMin
        percentPerRev = self.percentPerRev

        if percent > percentMax:
            logging.info(f"Over percentMax, moving to {percentMax}% (percentMax)")
            percentToMove = percentMax - currentPercent
            revToMove = percentToMove / percentPerRev
            rotate(revToMove)

            self.percent = percentMax

        elif percent < percentMin:
            logging.info(f"Under percentMin, moving to {percentMin}% (percentMin)")
            percentToMove = currentPercent - percentMin
            revToMove = percentToMove / percentPerRev
            rotate(revToMove)

            self.percent = percentMin
        
        else:
            percentToMove = percent - currentPercent
            revToMove = percentToMove / percentPerRev
            rotate(revToMove)

            self.percent = percent

        with open("stepper_loc.txt", "w") as location:
                location.write(str(self.percent))

def main():
    nema23 = StepperMotor(rps = 1, pulsePerRev = 1600)
    while True:
        value = input("Enter percentage to rotate to:")
        nema23.rotateTo(value)

if __name__ == "__main__":
    main()

from time import sleep
import RPi.GPIO as GPIO     # import GPIO library

GPIO.setmode(GPIO.BCM)

class stepper:
    def __init__(self, ena_pin, dir_pin, pul_pin, step_angle, dire='CW', speed=2):
        '''

        :param ena_pin:  rpi pin connect with driver en(-)
        :param dir_pin:  rpi pin connect with driver dir(-)
        :param pul_pin:  rpi pin connect with driver pul(-)
        :param step_angle: as per motor datasheet
        :param dire:      'CW' - clock wise   'CCW' - anticlockwise
        :param speed:    speed per second
        '''
        self.enable = ena_pin
        self.dire = dir_pin
        self.pulse = pul_pin
        self.step_angle = step_angle
        self.motor_stop = 26        # when this pin is low at time motor is pause/stop
        GPIO.setup(self.dire, GPIO.OUT)
        GPIO.setup(self.enable, GPIO.OUT)
        GPIO.setup(self.pulse, GPIO.OUT)
        GPIO.setup(self.motor_stop, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setwarnings(False)

        self.puls = (360.0 / step_angle)
        self.rps = speed
        self.pulse_in = self.rps * self.puls
        self.delay = (1 / (2 * self.pulse_in))
        GPIO.output(self.enable, GPIO.HIGH)

        if dire == 'CW':
            GPIO.output(self.dire, 1)
        else:
            GPIO.output(self.dire, 0)

    def main(self):
        while((GPIO.input(self.motor_stop))==1):
            GPIO.output(self.enable, GPIO.HIGH)
            for x in range(2 * int(self.pulse_in)):
                GPIO.output(self.pulse, GPIO.HIGH)
                sleep(self.delay)
                GPIO.output(self.pulse, GPIO.LOW)
                sleep(self.delay)
        GPIO.output(self.enable, GPIO.LOW)


if __name__ == '__main__':
    while 1:
        motor1 = stepper(ena_pin=16, dir_pin=20, pul_pin=21, step_angle=1.8, dire='CW', speed=10)
        motor1.main()


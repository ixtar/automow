

import RPi.GPIO as GPIO
from . import timer

GPIO.setmode(GPIO.BCM)  # BOARD pin-numbering scheme
# Pin Definitons:
echo = 17  # Board pin 11, BCM 17
trig = 18  # Board pin 12, BCM 18

class UltrasonicSensor():
    def init(self, echo_pin, trig_pin):
        # Pin Setup:
        GPIO.setup(trig_pin, GPIO.OUT)  # trigger pin set as output
        GPIO.setup(echo_pin, GPIO.IN)  # echo pin set as input
        self.echo_pin = echo_pin
        self.trig_pin = trig_pin
        # Initial state for trigger ping:
        GPIO.output(trig_pin, GPIO.LOW)
        #
        self.ultrasonic_timer = timer.Timer()

    def distance_to_obstacle(self):
        GPIO.output(self.trig_pin, GPIO.HIGH)
        # timer wait 10uS
        self.ultrasonic_timer.delay(9.5)
        # time.sleep()
        GPIO.output(self.trig_pin, GPIO.LOW)
        # timer start
        #
        self.ultrasonic_timer.start()
        GPIO.wait_for_edge(echo, GPIO.RISING)
        # timer stop here
        duration = self.ultrasonic_timer.get_difference()
        distance = duration * 0.034 / 2
        return distance
import pwm
import RPi.GPIO as jio
from time import sleep
def set_direction_pins():
    motor_pin_a = 18 # BOARD pin 12, BCM pin 18
    motor_pin_b = 16 # BOARD pin 16, BCM pin 16
    # Pin Setup:
    # Board pin-numbering scheme
    jio.setmode(jio.BOARD)
    # Set both pins LOW to keep the motor idle
    # You can keep one of them HIGH and the LOW to start with rotation in one direction
    jio.setup(motor_pin_a, jio.OUT, initial=jio.LOW)
    jio.setup(motor_pin_b, jio.OUT, initial=jio.LOW)

    print("Starting demo now! Press CTRL+C to exit")
    curr_value_pin_a = jio.HIGH
    curr_value_pin_b = jio.LOW

    # Toggle the output every second
    print("Outputting {} to pin {} AND {} to pin {}".format(curr_value_pin_a, motor_pin_a, curr_value_pin_b, motor_pin_b))
    jio.output(motor_pin_a, curr_value_pin_a)
    jio.output(motor_pin_b, curr_value_pin_b)


def main():
    set_direction_pins()
    # 200 is the lowest
    # each 1HZ is a step
    motor1 = pwm.Motor(350, 32, jio.LOW)
    motor2 = pwm.Motor(350, 33, jio.LOW)
    motor1.pwm.start(50)
    motor2.pwm.start(50)

    while True:
        motor1.set_speed(350, 1000)
        motor2.set_speed(350, 1000)
        while True:
            pass

try:
    main( )
except:
    jio.cleanup()
    print(Exception.with_traceback())
    print("\ncleaned up")

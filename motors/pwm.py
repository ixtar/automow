import RPi.GPIO as jio
from time import sleep
from yaml import safe_load
from motors.power_controller import PowerController
from motors import mower_motor

# CONFIG FILE LOOKS LIKE THIS:
# MOTOR_PINS:
#     RIGHT_SIDE: 
#         PWM_PIN: 
#           PIN_NUMBER: 32
#         DIRECTION_PINS:
#             BACK: 
#               PIN_NUMBER: 37
#             FRONT: 
#               PIN_NUMBER: 35
#     LEFT_SIDE: 
#         PWM_PIN: 
#           PIN_NUMBER: 33
#         DIRECTION_PINS:
#             BACK: 
#               PIN_NUMBER: 36
#             FRONT: 
#               PIN_NUMBER: 38
# POWER_CONTROL_PIN: 11
# MOWER_MOTOR_PIN: 22


BASELINE_FREQUENCY = 300 # frequency to prevent slipping when starting motors or changing directions
MOTOR_FORWARD = 0
MOTOR_BACKWARD = 1

class Motor():
    """
    Stepper motor class
    """
    def __init__(self, direction_pin):
        """
        Args:
            direction_pin (int): gpio pin nubmer responsible for motor
                                 direction multiplexer
        """
        # setup gpio
        jio.setup(direction_pin, jio.OUT, initial = MOTOR_FORWARD)
        self.current_direction_state = MOTOR_FORWARD
        self.direction_pin = direction_pin

    def change_direction(self):    
        self.current_direction_state ^= self.current_direction_state
        jio.output(self.direction_pin, self.current_direction_state)
    
    def set_foward(self):
        self.current_direction_state = MOTOR_FORWARD
        jio.output(self.direction_pin, self.current_direction_state)
    
    def set_backward(self):
        self.current_direction_state = MOTOR_BACKWARD
        jio.output(self.direction_pin, self.current_direction_state)

class Side():
    """
    One side of the Automow, controlling front and back motors
    """
    def __init__(self, pwm_frequency, SIDE_PIN_DICT):
        """
        prarams:
            pwm_frequency (int): initialization pwm frequency
        """
        self.motor_power_controller = PowerController()
        self.motor_power_controller.power_off()

        # extract direction pins dictionary
        DIRECTION_PINS_DICT = SIDE_PIN_DICT.get("DIRECTION_PINS")
        
        # extract front direction control pins
        self.front_direction_pin = DIRECTION_PINS_DICT.get("FRONT").get("PIN_NUMBER")
        # extract back direction control pins
        self.back_direction_pin = DIRECTION_PINS_DICT.get("BACK").get("PIN_NUMBER")
        
        # initialize back and fron motors for the side
        self.front_motor = Motor(self.front_direction_pin)
        self.back_motor = Motor(self.back_direction_pin)
        self.motors = [self.front_motor, self.back_motor]

        # set pwm speed control pin
        self.pwm_pin = SIDE_PIN_DICT.get("PWM_PIN").get("PIN_NUMBER")
        jio.setup(self.pwm_pin, jio.OUT, initial = jio.LOW)
        self.pwm = jio.PWM(self.pwm_pin, pwm_frequency)
        self.current_frequency = pwm_frequency

    def start_motors(self):
        # start motor movement with duty cycle 50 and with the origianlly set frequency
        self.pwm.start(50)
        self.pwm.ChangeDutyCycle(50)
        self.motor_power_controller.power_on()

    def stop_motors(self):
        self.motor_power_controller.power_off()
        self.pwm.ChangeDutyCycle(0)

    def change_frequency(self, frequency):
        self.pwm.ChangeFrequency(frequency)


class Body():
    """
    Automow body controlling two sides (four motors) at each corner of AutoMow body
    """
    def __init__(self):
        jio.setmode(jio.BOARD)
        with open('motors/motor_pin_definitions.yaml', 'r') as file:
            CONFIG = safe_load(file)
        MOTOR_PINS = CONFIG.get("MOTOR_PINS")
        self.left_side = Side(BASELINE_FREQUENCY, MOTOR_PINS.get("LEFT_SIDE"))
        self.right_side = Side(BASELINE_FREQUENCY, MOTOR_PINS.get("RIGHT_SIDE"))
        self.sides = [self.left_side, self.right_side]
        self.current_frequency = BASELINE_FREQUENCY
        
        MOWER_MOTOR_PIN = CONFIG.get("MOWER_MOTOR_PIN")
        self.mower_motor = mower_motor.MowerMotor(MOWER_MOTOR_PIN)

    def move(self):
        # launch motor movement
        for side in self.sides:
            side.start_motors()

    def move_forward(self):
        # always start with baseline to prevent slipping
        self.stop()
        sleep(0.2)

        self.change_speed(BASELINE_FREQUENCY, time_interval_between_increments=0)

        # Set all motors for forward operation
        for side in self.sides:
            for motor in side.motors:
                motor.set_foward()

        # start both pwm sides
        self.right_side.start_motors()
        self.left_side.start_motors()
        # reinstate preset speed 
        self.change_speed(self.current_frequency)
        
    def move_backward(self):
        # reverse motor direction
        self.stop()
        sleep(0.2) # delay to let the motors go to rest
        for side in self.sides:
            for motor in side.motors:
                motor.set_backward()
            side.start_motors()
    
    def stop(self):
        self.left_side.stop_motors()
        self.right_side.stop_motors()
    
    def change_speed(self, targ_frequency, time_interval_between_increments = 0.15):
        # gradually increase speed to prevent slipping
        while(self.current_frequency != targ_frequency):
            # decide increment change
            if (self.current_frequency < targ_frequency):
                self.current_frequency = self.current_frequency + 50
            if (self.current_frequency > targ_frequency):
                self.current_frequency = self.current_frequency - 50
            # change pwms frequency
            self.left_side.change_frequency(self.current_frequency)
            self.right_side.change_frequency(self.current_frequency)
            sleep(time_interval_between_increments)
    
    def spin_cw(self):
        # operate the wheels to spin automow
        self.stop()

        for motor in self.left_side.motors:
            motor.set_foward()
        for motor in self.right_side.motors:
            motor.set_backward()

        self.right_side.change_frequency(BASELINE_FREQUENCY)
        self.left_side.change_frequency(BASELINE_FREQUENCY)

        self.right_side.start_motors()
        self.left_side.start_motors()
        
        # do quarter rotation then stop
        sleep(1.2)
        self.stop()

    def spin_ccw(self):
        # operate the wheels to spin automow
        self.stop()

        for motor in self.right_side.motors:
            motor.set_foward()
        for motor in self.left_side.motors:
            motor.set_backward()

        self.right_side.change_frequency(BASELINE_FREQUENCY)
        self.left_side.change_frequency(BASELINE_FREQUENCY)

        self.right_side.start_motors()
        self.left_side.start_motors()
        
        # do quarter rotation then stop
        sleep(1.2)
        self.stop()

    def slide_right(self):
        self.stop()
        self.left_side.front_motor.set_foward()
        self.left_side.back_motor.set_backward()

        self.right_side.front_motor.set_backward()
        self.right_side.back_motor.set_foward()
        self.move()

    def slide_left(self):
        self.stop()
        self.right_side.front_motor.set_foward()
        self.right_side.back_motor.set_backward()

        self.left_side.front_motor.set_backward()
        self.left_side.back_motor.set_foward()
        self.move()
    
    def tunr_on_mower(self):
        self.mower_motor.turn_on()

    def tunr_off_mower(self):
        self.mower_motor.turn_off()

    def clean_up(self):
        jio.cleanup()
        print("cleaned up")
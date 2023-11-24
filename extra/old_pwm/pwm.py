import RPi.GPIO as jio
import time

motor_pin_a = 18 # BOARD pin 12, BCM pin 18
motor_pin_b = 23 # BOARD pin 16, BCM pin 16



class Motor():
    def __init__(self, freq, output_pin, initial_state):


        # Pin Setup:
        # Board pin-numbering scheme
        # Set both pins LOW to keep the motor idle
        # You can keep one of them HIGH and the LOW to start with rotation in one direction
        jio.setup(output_pin, jio.OUT, initial = initial_state)
        # self.pwm = jio.PWM(output_pin, freq)
        self.pwm = jio.PWM(output_pin, freq)

    def set_speed(self, current_freq, freq):
        # current_freq = self.pwm._frequency_hz
        while (current_freq != freq):
            if (current_freq < freq):
                current_freq = current_freq + 50
                self.pwm.ChangeFrequency(current_freq)
            if (current_freq > freq):
                current_freq = current_freq - 50
                self.pwm.ChangeFrequency(current_freq)
            time.sleep(0.5)
        print("speed reached")
        

    # def set_speed(self):
    #     val = 25
    #     incr = 5

    #     print("PWM running. Press CTRL+C to exit.")
    #     while True:
    #         time.sleep(0.25)
    #         if val >= 100 or val <= 0:
    #             incr = -incr
    #         val += incr
    #         self.pwm.ChangeFrequency(val)
    #         print(val)

    # def change_direction(self):
    #     pass


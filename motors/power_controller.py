from yaml import safe_load
import RPi.GPIO as jio

class PowerController():
    def __init__(self):
        with open('motors/motor_pin_definitions.yaml', 'r') as file:
            CONFIG = safe_load(file)
        self.pin = CONFIG.get("POWER_CONTROL_PIN")
        jio.setup(self.pin, jio.OUT, initial = jio.LOW)
    
    def power_on(self):
        jio.output(self.pin, jio.HIGH)
    
    def power_off(self):    
        jio.output(self.pin, jio.LOW)

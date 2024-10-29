Two phase quad stepper motor control using jetson nano and L298N dual 
h-bridge motor controllers additional motor control logic circuitry needs
to be setup according to the wiring diagram in motor_logic_circuit.png

Jetson connection to motor control circuitry according to jetson_setup.png
pin configuration can be changed through motor_pin_definitions.yaml in 
motors directory

use pwm.py to control body movement through the body class.

use serial_ultrasonic.py in serial_ultrasonic/i2c
to poll ultrasonic sensor through an i2c connected arduino

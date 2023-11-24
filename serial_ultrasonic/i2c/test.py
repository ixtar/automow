import smbus
import serial_ultrasonic

# Create an smbus object (you might need to change the bus number)
bus = smbus.SMBus(1)

while True:
    ultraonic_sonic = serial_ultrasonic.ultrasonicSensor(bus)
    distance = ultraonic_sonic.get_ultrasonic_distance()
    print(distance)
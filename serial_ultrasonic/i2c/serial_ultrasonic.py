from time import sleep

# I2C address of the Arduino peripheral
ARDUINO_ADDRESS = 11

# Function to send an integer via I2C
def send_integer(bus, data):
    bus.write_byte(ARDUINO_ADDRESS, data)
    print(f"Sent: {data}")

# Function to receive an integer via I2C
def receive_integer(bus):
    received_data = bus.read_byte(ARDUINO_ADDRESS)
    return received_data

class ultrasonicSensor():
    """
    Abstraction layer for the ultrasonic sensor
        distance is pulled from the arduino through i2c
    """
    def __init__(self, bus):
        self.bus = bus

    def get_ultrasonic_distance(self, direction = 1):
        """
        args:
            (int) direction: describes the direction of scanning
                1 - forward direction scanning
                2 - left direction scanning
                3 - right direction scanning
        """
        send_integer(self.bus, direction)
        sleep(0.05)
        distance = receive_integer(self.bus)
        return distance
        
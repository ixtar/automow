from time import sleep

# I2C address of the Arduino peripheral
ARDUINO_ADDRESS = 11

# Function to send an integer via I2C
def send_integer(bus, data):
    """
    Send one uint8 through an I2C bus
    args:
        (SMBUS::bus) bus: i2c bus object
        (uint8) data: to send through the bus 
    """
    bus.write_byte(ARDUINO_ADDRESS, data)

# Function to receive an integer via I2C
def receive_integer(bus):
    """
    Recieve one uint8 through an I2C bus
    args:
        bus: SMBUS i2c bus object
    """
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
        returns:
            distance in CM to the closest obstacle in the chosen direction
            (with 15 degrees spread)
        """
        send_integer(self.bus, direction)
        distance = receive_integer(self.bus)
        return distance
    
    def get_lfr_distances(self):
        """
        returns distances from three directions through ultrasonic sensor
        takes about 20ms to execute 
        reurns:
            tuple of distances to the closest obstacle (left, front, right)
        """
        distance_front = self.get_ultrasonic_distance(1)
        sleep(0.01)
        distance_left = self.get_ultrasonic_distance(2)
        sleep(0.01)
        distance_right = self.get_ultrasonic_distance(3)

        # tuple designed by nakul 
        distances = (distance_left, distance_front, distance_right)
        return distances


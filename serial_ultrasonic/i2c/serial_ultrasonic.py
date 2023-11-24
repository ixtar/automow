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
    def __init__(self, bus):
        self.bus = bus

    def get_ultrasonic_distance(self):
        send_integer(self.bus, 1)
        sleep(0.05)
        distance = receive_integer(self.bus)
        return distance
        
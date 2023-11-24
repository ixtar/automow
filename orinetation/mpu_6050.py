import smbus					#import SMBus module of I2C
from time import sleep 

# Register Addresses
PWR_MGMT_1   = 0x6B
SMPLRT_DIV   = 0x19
CONFIG       = 0x1A
GYRO_CONFIG  = 0x1B
INT_ENABLE   = 0x38
ACCEL_XOUT_H = 0x3B
ACCEL_YOUT_H = 0x3D
ACCEL_ZOUT_H = 0x3F
GYRO_XOUT_H  = 0x43
GYRO_YOUT_H  = 0x45
GYRO_ZOUT_H  = 0x47

def read_raw_data(addr, bus):
    """
    Read output form register with address addr
    Args:
        (int) addr: address of the register to read
        (SMBus) bus: serial bus object
    """
    Device_Address = 0x68   # MPU6050 device address 
	#Temperature, Accelero, Gyro values are 16-bit
    high = bus.read_byte_data(Device_Address, addr)
    low = bus.read_byte_data(Device_Address, addr+1)

    #concatenate higher and lower value
    value = ((high << 8) | low)
    
    #to get signed value from mpu6050
    if(value > 32768):
        value = value - 65536
    return value

class MPU():
    """
    Abstraction layer for MPU6050 temperature sensor
    """
    def __init__(self, bus):
        """
        Initialize and configure MPU to continous temperature measurements

        Args:
            (SMBus) bus: serial bus object
        """
        #some MPU6050 Registers and their Address

        Device_Address = 0x68   # MPU6050 device address 

        #write to sample rate register
        bus.write_byte_data(Device_Address, SMPLRT_DIV, 7)

        #Write to power management register
        bus.write_byte_data(Device_Address, PWR_MGMT_1, 1)

        #Write to Configuration register
        bus.write_byte_data(Device_Address, CONFIG, 0)

        #Write to Gyro configuration register
        bus.write_byte_data(Device_Address, GYRO_CONFIG, 24)

        #Write to interrupt enable register
        bus.write_byte_data(Device_Address, INT_ENABLE, 1)

    def read_temperature(self, bus):
        """
        Read temperature output form MPU6050
        Args:
            (SMBus) bus: serial bus object
        """
        TEMP_OUT_H = 0x41 # MSBs of temperature reading [15:8]
        temperature = read_raw_data(TEMP_OUT_H, bus)
        # convert raw data to temperature in degrees C
        temperature = float(temperature)/340+36.53
        return temperature
    
    def track_orinettation(self, bus):
        acc_x = read_raw_data(ACCEL_XOUT_H, bus)
        acc_y = read_raw_data(ACCEL_YOUT_H, bus)
        acc_z = read_raw_data(ACCEL_ZOUT_H, bus)

        #Read Gyroscope raw value
        gyro_x = read_raw_data(GYRO_XOUT_H, bus)
        gyro_y = read_raw_data(GYRO_YOUT_H, bus)
        gyro_z = read_raw_data(GYRO_ZOUT_H, bus)
        
        #Full scale range +/- 250 degree/C as per sensitivity scale factor
        Ax = acc_x/16384.0
        Ay = acc_y/16384.0
        Az = acc_z/16384.0
        accel = (Ax, Ay, Az)
        
        Gx = gyro_x/131.0
        Gy = gyro_y/131.0
        Gz = gyro_z/131.0
        gyro = (Gx, Gy, Gz)
        
        return {"accelormeter": accel, "gyrometer": gyro} 
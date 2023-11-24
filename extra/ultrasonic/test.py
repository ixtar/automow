from . import ultrasonic
import RPi.GPIO as GPIO
import time

def main():
    GPIO.setmode(GPIO.BCM)
    echo = 17  # Board pin 11, BCM 17
    trig = 18  # Board pin 12, BCM 18
    ultrasonicSensor = ultrasonic.UltrasonicSensor(echo, trig)
    time.sleep(1)
    try:
        while True:
            distance_to_obstacle = ultrasonicSensor.distance_to_obstacle()
            print(distance_to_obstacle)
    finally:
        GPIO.cleanup()

if __name__ == '__main__':
    main()
from motors import pwm
from time import sleep

def test():
    try:
        # motor initialize body
        body = pwm.Body()
        body.move_forward()
        body.mower_motor.turn_on()
        sleep(5)
        body.move_backward()
        body.mower_motor.turn_off()
        sleep(5)
    
    finally:
        body.clean_up()

if __name__ == "__main__":
    while True:
        test()
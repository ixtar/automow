import sys
import tty
import termios
from motors import pwm
import RPi.GPIO as jio
import traceback

def get_first_letter():
    print("Press any key: ", end='', flush=True)

    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)

    try:
        tty.setraw(fd)
        key = sys.stdin.read(1)
        return key
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)

class Controller():
    def run():
        body = pwm.Body()
        # Call the function
        while True:
            command = get_first_letter()
            
            if command == "l":
                exit()

            elif command == "w":
                body.move_forward()
                print("moving forward")
            
            elif command == "s":
                body.move_backward()
                print("moving backward")
            
            elif command == " ":
                body.stop()
            
            elif command == "d":
                body.spin_cw()            
            elif command == "a":
                body.spin_ccw()


            elif command == "p":
                body.slide_right()

            elif command == "o":
                body.slide_left()
            
            
            
            elif command == "u":
                body.change_speed(body.right_side.current_frequency + 100)

            elif command == "j":
                body.change_speed(body.right_side.current_frequency - 100)

            
            else:
                print(f"{command} is not a valid input")

try:
    Controller.run()

except Exception as e:
    print(traceback.format_exc())


finally:
    jio.cleanup()
                  

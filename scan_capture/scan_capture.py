import sys
import tty
import termios
from ..motors import pwm

def get_first_letter():
    print("\n", end='', flush=True)

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
                body.spin_cw
            
            elif command == "a":
                body.spin_ccw

            if command == "u":
                body.change_speed(body.right_side.current_frequency + 25)

            if command == "j":
                body.change_speed(body.right_side.current_frequency - 25)

            else:
                print(f"{command} is not a valid input")

            
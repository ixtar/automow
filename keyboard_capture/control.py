import keyboard
from ..motors import pwm

class Controller():
    def __init__(self) -> None:
        # Initialize AutoMow Body
        self.body = pwm.Body()

        keyboard.add_hotkey("w", self.body.move_forward())
        keyboard.add_hotkey("s", self.body.move_backward())
        keyboard.add_hotkey(" ", self.body.stop())
        keyboard.add_hotkey("d", self.body.spin_cw())
        keyboard.add_hotkey("a", self.body.spin_cw())
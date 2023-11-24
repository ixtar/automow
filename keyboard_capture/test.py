import keyboard

class Controller():
    def __init__(self) -> None:
        # Initialize AutoMow Body
        keyboard.add_hotkey("w", lambda: print("nigga pressed w"))
        keyboard.add_hotkey("s", lambda: print("nigga pressed s"))
        keyboard.add_hotkey(" ", lambda: print("nigga pressed space"))


controller = Controller()

while True:
    pass
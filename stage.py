import time
import pyautogui
import random
import json

class jam():
    def __init__(self, height, width) -> None:
        self.height = height
        self.width = width
        self.pause_duration = 0.5

    def open_reel(self):
        time.sleep(self.pause_duration)
        pyautogui.keyDown("b")
        time.sleep(self.pause_duration)
    
    def close_reel(self):
        time.sleep(self.pause_duration)
        pyautogui.keyUp("b")
        time.sleep(self.pause_duration)
    
    def change_instrument(self):
        self.open_reel()
        pyautogui.moveTo(self.width / 2, self.height / 2)
        pyautogui.click()
        self.close_reel()  

    def change_song(self):
        with open("positions.json") as f:
            dump = json.load(f)
        
        reel_outer = dump[str(self.height)]
        
        rand_reel = reel_outer[random.randint(0, len(reel_outer) - 1)]

        self.open_reel()
        time.sleep(self.pause_duration)
        pyautogui.moveTo(rand_reel[0], rand_reel[1])
        pyautogui.click() # Selects random song
        self.close_reel()
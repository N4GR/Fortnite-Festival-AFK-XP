import pyautogui, random, time
import psutil, pygetwindow
from tqdm import tqdm

class checks():
    def active(service_name: str) -> bool:
        '''
        Function that checks if a service is running by given naming, returning True if it is and False if it isn't.

        service_name: str (The name of the service to check)

        -> bool (True or False if the service is running.)
        '''
        if service_name in (i.name() for i in psutil.process_iter()): # Returns bool if service_name is found in active services.
            return True
        else:
            return False

class jam():
    def __init__(self, game_height, game_width) -> None:
        self.height = game_height
        self.width = game_width
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
        reel_outer = [[1899, 503], 
                      [2283, 680], 
                      [2461, 1046], 
                      [2283, 1432], 
                      [1899, 1604], 
                      [1500, 1448], 
                      [1400, 1046]]
        
        rand_reel = reel_outer[random.randint(0, len(reel_outer) - 1)]

        self.open_reel()
        time.sleep(self.pause_duration)
        pyautogui.moveTo(rand_reel[0], rand_reel[1])
        pyautogui.click() # Selects random song
        self.close_reel()
    
active = checks.active("FortniteClient-Win64-Shipping.exe")

if active is False:
    print("Fortnite isn't running, open fortnite and restart the program.")
    exit()
else:
    #game_height, game_width = fullscreen
    game_height = 2160
    game_width = 3840

def main():
    time_ran = 0

    while True:
        jam(game_height, game_width).change_instrument()
        jam(game_height, game_width).change_song()

        print(f"Waiting 60 seconds...\nRan {time_ran} times.")
        for x in tqdm(range(60)):
            time.sleep(1)

        time_ran+=1

if __name__ == "__main__":
    main()
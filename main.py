import time
import psutil
from tqdm import tqdm

from stage import jam
from screeninfo import get_monitors

import pyautogui
import cv2
import easyocr

import json
import os

def getMainMonitor():
    for m in get_monitors():
        if m.is_primary is True:
            return m

class checks():
    def __init__(self) -> None:
        self.client_name = "FortniteClient-Win64-Shipping.exe"
        self.active()
        
    def active(self) -> bool:
        '''
        Function that checks if a service is running by given name, returning True if it is and False if it isn't.

        -> bool (True or False if the service is running.)
        '''
        if self.client_name in (i.name() for i in psutil.process_iter()): # Returns bool if service_name is found in active services.
            monitor = getMainMonitor()
            
            return monitor.height, monitor.width
        
        else:
            print("Fortnite isn't running, open fortnite and restart the program.")
            exit()

class disconnect():
    def __init__(self) -> None:
        self.monitor = getMainMonitor()

        with open("discpos.json") as f:
            self.dump = json.load(f)
    
    def beginLoop(self):
        times_ran = 0
        if self.reconnect() is True:
            while True:
                if self.CheckTrueReconnect() is True:
                    print(f"Success! You've been reconnected...\nIt took {times_ran * 5} seconds to reconnect you.\n")
                    return True

                times_ran += 1

                print(f"Checked {times_ran} time/s if you've been successfully reconnected.")
                time.sleep(5)
                
        else:
            print("There was an error reconnecting, exitting program.")
            os._exit(0)
            

    def checkTrue(self) -> bool:
        screenshot_conf = self.dump[str(self.monitor.height)]["screenshot"]

        img1 = pyautogui.screenshot(region=(screenshot_conf[0], screenshot_conf[1], screenshot_conf[2], screenshot_conf[3]))
        img1.save("dump/check_disconnect.png")
        img = cv2.imread("dump/check_disconnect.png")

        # Text detect instance
        reader = easyocr.Reader(["en"], gpu = False, verbose = False)

        # Detect text
        detect = reader.readtext(img)

        if not detect:
            return False
        else:
            for t in detect:
                bbox, text, score = t

                if text == "PLAY":
                    return True

    def reconnect(self) -> bool:
        try:
            reconnect_conf = self.dump[str(self.monitor.height)]["reconnect"]

            pyautogui.dragTo(reconnect_conf[0], reconnect_conf[1])
            time.sleep(1)
            pyautogui.click()
        except Exception as error:
            print(error)
            return False

        return True
    
    def CheckTrueReconnect(self) -> bool:
        screenshot_conf = self.dump[str(self.monitor.height)]["check_reconnect"]

        img1 = pyautogui.screenshot(region=(screenshot_conf[0], screenshot_conf[1], screenshot_conf[2], screenshot_conf[3]))
        img1.save("dump/reconnect_check.png")
        img = cv2.imread("dump/reconnect_check.png")

        # Text detect instance
        reader = easyocr.Reader(["en"], gpu = False, verbose = False)

        # Detect text
        detect = reader.readtext(img)  
 

        if not detect:
            return False
        else:
            for t in detect:
                bbox, text, score = t

                if text == "Play Loop":
                    return True

def main():
    height, width = checks().active()
    discon = disconnect()

    time_ran = 0

    while True:
        jam(height, width).change_instrument()
        jam(height, width).change_song()

        print(f"Waiting 60 seconds...\nRan {time_ran} times.")
        for x in tqdm(range(60)):
            time.sleep(1)

        if discon.checkTrue() is True:
            print("You've been disconnected, trying to reconnect now...")
            discon.beginLoop()

        time_ran += 1

        print(f"Checked {time_ran} time/s if you've been disconnected...")

if __name__ == "__main__":
    main()
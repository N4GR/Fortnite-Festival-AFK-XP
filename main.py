import time
import psutil
from tqdm import tqdm

from stage import jam
from screeninfo import get_monitors

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
            for m in get_monitors():
                if m.is_primary is True:
                    monitor = m
            
            return monitor.height, monitor.width
        
        else:
            print("Fortnite isn't running, open fortnite and restart the program.")
            exit()

def main():
    height, width = checks().active()

    time_ran = 0

    while True:
        jam(height, width).change_instrument()
        jam(height, width).change_song()

        print(f"Waiting 60 seconds...\nRan {time_ran} times.")
        for x in tqdm(range(60)):
            time.sleep(1)

        time_ran+=1

if __name__ == "__main__":
    main()
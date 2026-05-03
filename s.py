import minescript
import time
import random
import keyboard
import threading
from combinedm import macro_check_monitor, stop

import Share
import os

#############################################################################
#MacroCheck settings
#############################################################################

settings = {
    "yaw": 135,
    "pitch": 0,
}

#############################################################################
#farming settings
#############################################################################
lane = 48 #time in seconds to walk one lane
#kill script
def kill():
    while True:
        if keyboard.is_pressed('-'):
            stop()
            break
        time.sleep(1.2)

#############################################################################
#functions to move left and right
#############################################################################


def moveb():
    try:
        minescript.player_press_left(True)
        time.sleep(lane + random.uniform(0.05, 0.11))
    finally:
        minescript.player_press_left(False)

def movef():
    try:
        minescript.player_press_forward(True)
        time.sleep(lane + random.uniform(0.05, 0.11))
    finally:
        minescript.player_press_forward(False)

def moves():
    minescript.player_press_left(True)
    time.sleep(random.uniform(0.3, 0.4))
    minescript.player_press_left(False)





def main():
    Share.running = True
    Share.prev_pos = None
    minescript.player_press_attack(True)
    for i in range(6):
        if i == 5:   # 5th loop (0-based index)
            movef()
        else:
            movef()
            time.sleep(random.uniform(0.018, 0.025))
            moveb()
            time.sleep(random.uniform(0.018, 0.025))

    Share.running = False
    minescript.player_press_attack(False)
    time.sleep(random.uniform(0.32, 0.51))
    minescript.player_inventory_select_slot(3)
    time.sleep(random.uniform(0.32, 0.51))
    minescript.player_press_use(True)
    time.sleep(random.uniform(0.02,0.05))
    minescript.player_press_use(False)
    time.sleep(random.uniform(0.32, 0.51))
    minescript.player_inventory_select_slot(5)




if __name__ == "__main__":
        threading.Thread(target=kill, daemon=True).start()
        #macrocheck threads
        threading.Thread(target=macro_check_monitor, args=(settings,), daemon=True).start()
        main()
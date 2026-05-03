import minescript
import time
import random
import keyboard
import threading
from combinedm import stop, macro_check_monitor
import Share

#############################################################################
#MacroCheck settings
#############################################################################

settings = {
    "yaw": 180,
    "pitch": 68,
}

#############################################################################
#farming settings
#############################################################################
lane = 80 #time in seconds to walk one lane
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
        minescript.player_press_backward(True)
        time.sleep(lane + random.uniform(0.12, 0.31))
    finally:
        minescript.player_press_backward(False)

def movef():
    try:
        minescript.player_press_forward(True)
        time.sleep(lane + random.uniform(0.12, 0.31))
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
    for i in range(5):
        movef()
        time.sleep(random.uniform(0.018, 0.025))
        moves()
        time.sleep(random.uniform(0.018, 0.025))
        moveb()
        time.sleep(random.uniform(0.018, 0.025))
        if i != 4:  # skip the last one (since range(9) goes 0–8)
            moves()

    Share.running = False
    minescript.player_press_attack(False)
    time.sleep(random.uniform(0.12, 0.31))
    minescript.player_inventory_select_slot(3)
    time.sleep(random.uniform(0.12,0.31))
    minescript.player_press_use(True)
    time.sleep(random.uniform(0.02,0.05))
    minescript.player_press_use(False)
    time.sleep(random.uniform(0.15, 0.25))
    minescript.player_inventory_select_slot(5)




if __name__ == "__main__":
        threading.Thread(target=kill, daemon=True).start()
        #macrocheck threads
        threading.Thread(target=macro_check_monitor, args=(settings,), daemon=True).start()
        main()
import minescript
import time
import random
import keyboard
import threading
from combinedm import macro_check_monitor, stop
import Share

#############################################################################
#MacroCheck settings
#############################################################################

settings = {
    "yaw": -90,
    "pitch": -59,
}

#############################################################################
#farming settings
#############################################################################
lane = 66 #time in seconds to walk one lane
#kill script
def kill():
    while True:
        if keyboard.is_pressed('-'):
            stop()
            break
        time.sleep(0.5)

#############################################################################
#functions to move left and right
#############################################################################


def moveL():
    try:
        minescript.player_press_left(True)
        minescript.player_press_forward(True)
        time.sleep(lane + random.uniform(0.62, 0.71))
    finally:
        minescript.player_press_backward(False)
        minescript.player_press_left(False)

def moveR():
    try:
        minescript.player_press_right(True)
        minescript.player_press_forward(True)
        time.sleep(lane + random.uniform(0.62, 0.71))
    finally:
        minescript.player_press_forward(False)
        minescript.player_press_right(False)





def main():
    Share.running = True
    Share.prev_pos = None
    minescript.player_press_attack(True)
    for i in range(4):
        moveL()
        time.sleep(random.uniform(0.018, 0.025))
        moveR()
        time.sleep(random.uniform(0.018, 0.025))

    Share.running = False
    minescript.player_press_attack(False)
    time.sleep(random.uniform(0.8, 1.2))
    minescript.player_inventory_select_slot(3)
    time.sleep(random.uniform(0.32,0.41))
    minescript.player_press_use(True)
    time.sleep(random.uniform(0.02,0.05))
    minescript.player_press_use(False)
    time.sleep(random.uniform(0.25, 0.45))
    minescript.player_inventory_select_slot(5)




if __name__ == "__main__":
        threading.Thread(target=kill, daemon=True).start()
        #macrocheck threads
        threading.Thread(target=macro_check_monitor, args=(settings,), daemon=True).start()
        main()
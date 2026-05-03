import minescript as m
import time
import random

def stop():
    m.player_press_attack(False)
    m.player_press_left(False)
    m.player_press_right(False)
    m.player_press_forward(False)
    m.player_press_backward(False)
    m.execute("\killjob -1")




def macro_check_monitor(settings):
    """Check yaw/pitch, sudden teleport detection, and blocked detection."""
    global prev_pos
    # ===================================================================
    yaw_target = settings['yaw']
    pitch_target = settings['pitch']
    threshold = 15 
    # ===================================================================
    
    # Blocked detection variables
    blocked_pos = m.player_position()
    blocked_time = time.time()

    prev_pos = m.player_position()

    while True:
        yaw0, pitch0 = m.player_orientation()

        # Yaw/Pitch check
        if abs(yaw_target - yaw0) > 2.0 or abs(pitch_target - pitch0) > 2.0:
            m.echo("[MACRO CHECK] Yaw or pitch changed! Stopping script.")
            time.sleep(random.uniform(2.5, 3.5))
            stop()
            break

        pos = m.player_position()
        
        # Teleport detection
        dx = abs(pos[0] - prev_pos[0])
        dy = abs(pos[1] - prev_pos[1])
        dz = abs(pos[2] - prev_pos[2])
        
        if dx > threshold or dy > threshold or dz > threshold:
            m.echo("[MACRO CHECK] Sudden position change detected! Stopping script.")
            stop()

            break
        
        # Blocked detection - check if player hasn't moved for 10 seconds
        blocked_dx = abs(pos[0] - blocked_pos[0])
        blocked_dy = abs(pos[1] - blocked_pos[1])
        blocked_dz = abs(pos[2] - blocked_pos[2])
        
        if blocked_dx < 0.1 and blocked_dy < 0.1 and blocked_dz < 0.1:
            # Player hasn't moved significantly
            if time.time() - blocked_time > 5.0:
                m.echo("[MACRO CHECK] Player blocked (no movement for 15s)! Stopping script.")
                stop()
                break
        else:
            # Player has moved, reset blocked timer
            blocked_pos = pos
            blocked_time = time.time()

        prev_pos = pos
        time.sleep(0.2)

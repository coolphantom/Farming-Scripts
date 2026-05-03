import minescript as m
from minescript import EventQueue, EventType
from minescript_plus import Util 
import threading
import random
import time

START_POS = (-91.7, 75, 238.7)
END_POS = (-91.7, 67, -238.7)     # End position

# Layer Y positions
LAYER_Y_POSITIONS = [75, 73, 71, 69, 67]

# Safety
POSITION_CHANGE_THRESHOLD = 10

# Timing
BETWEEN_RUN_DELAY = random.randint(650, 1200)

# ===== FARMING SYSTEM =====
running = False
stop_event = threading.Event()

def warning(sound_name):
    """Play sound 3 times quickly"""
    for i in range(3):
        Util.play_sound(sound_name)
        time.sleep(0.4)

def wait(ms: int):
    step = 50
    elapsed = 0
    while elapsed < ms and running and not stop_event.is_set():
        stop_event.wait(step / 1000.0)
        if not running:
            break
        elapsed += step

def random_wait(min_ms, max_ms):
    wait_time = random.randint(min_ms, max_ms)
    wait(wait_time)

def reached_end(pos):
    """Check if we reached the final end position"""
    return (abs(pos[0] - END_POS[0]) < 1.0 and 
            abs(pos[1] - END_POS[1]) < 1.0 and 
            abs(pos[2] - END_POS[2]) < 1.0)

def farm_single_run(start_facing):
    """Farm one complete run through all layers in specified direction"""
    
    current_layer = 0
    
    while current_layer < 5 and running and not stop_event.is_set():
        
        # Ensure clean state before starting new layer
        time.sleep(random.uniform(0.12, 0.15))
        m.player_press_left(False)
        m.player_press_right(False)
        time.sleep(random.uniform(0.022, 0.031)) # Brief pause to ensure keys are released

        if not farm_current_layer(start_facing, current_layer):
            break
            
        current_pos = m.player_position()
        if reached_end(current_pos):
            break
            
        current_layer += 1
        if current_layer < 5 and running and not stop_event.is_set():
            time.sleep(random.uniform(0.32, 0.35))  # Longer delay for stability
    
    return True

def farm_current_layer(start_facing, layer_index):
    """Farm one layer by moving in one direction until height changes or reach end"""
    
    # Give a moment to stabilize position

    
    start_y = m.player_position()[1]
    
    m.player_press_attack(True)
    
    move_north = (layer_index % 2 == 0)
    
    m.player_press_left(False)
    m.player_press_right(False)
    
    if start_facing == "left":
        if move_north:
            m.player_press_left(True)   
        else:
            m.player_press_right(True)  
    else:  
        if move_north:
            m.player_press_right(True)  
        else:
            m.player_press_left(True)   
    
    warned_near_end = False

    while running and not stop_event.is_set():
        current_pos = m.player_position()
        current_y = current_pos[1]
        
        if layer_index == 4:
            close_to_end = ((current_pos[0] - END_POS[0]) ** 2 + (current_pos[2] - END_POS[2]) ** 2) ** 0.5
            if not warned_near_end and close_to_end < 10:
                warning(Util.get_soundevents().BELL_BLOCK)
                warned_near_end = True

        if current_y < start_y - 0.5:
            time.sleep(random.uniform(0.02, 0.05))
            break

        if reached_end(current_pos):
            m.echo("End reached")
            random_wait(200, 500)
            m.player_press_attack(False)
            m.player_press_left(False)
            m.player_press_right(False)
            time.sleep(random.uniform(0.12, 0.31))
            m.execute("warp Garden")
            time.sleep(random.uniform(1.2, 1.7))
            m.player_inventory_select_slot(3)
            time.sleep(random.uniform(0.012, 0.031))
            m.player_press_use(True)
            time.sleep(random.uniform(0.02, 0.05))
            m.player_press_use(False)
            time.sleep(random.uniform(0.15, 0.25))
            m.player_inventory_select_slot(5)
            break
        
        wait(50)  # Small delay to prevent tight loop
    
    m.player_press_left(False)
    m.player_press_right(False)
    
    return running

# ===== MAIN FARMING FUNCTION =====
def farming(start_facing):
    global running
    running = True
    stop_event.clear()
    
    try:         
        farm_single_run(start_facing)
                    
    finally:
        m.player_press_attack(False)
        m.player_press_left(False)
        m.player_press_right(False)
        running = False

# ===== SAFETY SYSTEMS =====
def safety_monitor():
    global running
    prev_pos = m.player_position()
    prev_pitch = m.player_orientation()[1]
    prev_yaw = m.player_orientation()[0]

    while running and not stop_event.is_set():
        current_pos = m.player_position()
        current_yaw, current_pitch = m.player_orientation()
        
        dx = abs(current_pos[0] - prev_pos[0])
        dy = abs(current_pos[1] - prev_pos[1])
        dz = abs(current_pos[2] - prev_pos[2])
        
        if (dx > POSITION_CHANGE_THRESHOLD or dy > POSITION_CHANGE_THRESHOLD or dz > POSITION_CHANGE_THRESHOLD):
            m.echo("Sudden position change detected! Stopping.")
            time.sleep(random.uniform(0.15, 0.25))
            running = False
            stop_event.set()
            warning(Util.get_soundevents().ENDER_DRAGON_GROWL)
            break
        
        pitch_change = abs(current_pitch - prev_pitch)
        if pitch_change > 2:  
            m.echo("Sudden pitch change detected! Stopping.")
            time.sleep(random.uniform(0.15, 0.25))
            running = False
            stop_event.set()
            warning(Util.get_soundevents().ENDER_DRAGON_GROWL)
            break
        
        yaw_change = abs(current_yaw - prev_yaw)
        if yaw_change > 15:  
            m.echo("Sudden yaw change detected! Stopping.")
            time.sleep(random.uniform(0.15, 0.25))
            running = False
            stop_event.set()
            warning(Util.get_soundevents().ENDER_DRAGON_GROWL)
            break

        prev_pos = current_pos
        prev_pitch = current_pitch
        prev_yaw = prev_yaw
        stop_event.wait(0.05)

def check_blocked():
    """Check if player is stuck when they should be moving"""
    global running
    last_pos = m.player_position()
    stuck_count = 0
    
    while running and not stop_event.is_set():
        stop_event.wait(0.1)  
        
        current_pos = m.player_position()
        dx = abs(current_pos[0] - last_pos[0])
        dz = abs(current_pos[2] - last_pos[2])
        
        if dx < 0.1 and dz < 0.1:
            stuck_count += 1
            
        if stuck_count >= random.randint(6, 8):  
            m.echo("Blocked! Stopping farming.")
            running = False
            stop_event.set()
            warning(Util.get_soundevents().ENDER_DRAGON_GROWL)
            break

        else:
            stuck_count = 0  
                
        last_pos = current_pos


def emergency_stop():
    """Force stop everything immediately"""
    global running
    running = False
    stop_event.set()
    
    m.player_press_attack(False)
    m.player_press_left(False)
    m.player_press_right(False)
    m.player_press_forward(False)
    

# ===== EVENT HANDLING =====
with EventQueue() as event_queue:
    event_queue.register_key_listener()
    m.echo("Script Loaded")
    m.echo("LEFT arrow to farm left")
    m.echo("RIGHT arrow to farm right") 
    m.echo("rshift for emergency stop")
    
    while True:
        event = event_queue.get()
        if event.type == EventType.KEY:
            # LEFT arrow to farm left
            if event.key == 263 and event.action == 1 and not running: 
                m.echo("Starting to farm LEFT")
                farming_thread = threading.Thread(target=farming, args=("left",), daemon=True)
                safety_thread = threading.Thread(target=safety_monitor, daemon=True)
                blocked_thread = threading.Thread(target=check_blocked, daemon=True)

                farming_thread.start()
                safety_thread.start()
                blocked_thread.start()
                
            # RIGHT arrow to farm right
            elif event.key == 262 and event.action == 1 and not running:  
                m.echo("Starting to farm RIGHT")
                farming_thread = threading.Thread(target=farming, args=("right",), daemon=True)
                safety_thread = threading.Thread(target=safety_monitor, daemon=True)
                blocked_thread = threading.Thread(target=check_blocked, daemon=True)

                farming_thread.start()
                safety_thread.start()
                blocked_thread.start()

                
            # Right Shift to stop (emergency)
            elif event.key == 344 and event.action == 1 and running:  
                m.echo("Emergency Stop")
                emergency_stop()
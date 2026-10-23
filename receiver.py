import socket
import sys
import time

from pynput.mouse import Controller, Button

mouse = Controller()

PORT = 5005
FIELDS = 5               
RESTART_GAP = 100        
PRINT_EVERY = 7       

CALIBRATION_SAMPLES = 100 

SENSITIVITY = 30.0       
#DEADZONE = 0.2      
SMOOTHING = 0.92

INVERT_X = False
INVERT_Y = True
INVERT_TILT = False

CLICK_THRESHOLD = 0.5
CLICK_COOLDOWN = 0.6
RETURN_LOCKOUT = 1.2


def parse(data):
    try:
        parts = data.decode().strip().split(",")
        if len(parts) != FIELDS:
            return None
        seq = int(parts[0])
        t, gx, gy, gz = map(float, parts[1:])
        return seq, t, gx, gy, gz
    except (UnicodeDecodeError, ValueError):
        return None


def deadzone(value):
    #if abs(value) < DEADZONE:
    #    return 0.0    
    return value


def main():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(("0.0.0.0", PORT))
    print(f"Listening on UDP port {PORT}...")
    print("Keep your head still while calibrating.")

    last_seq = -1
    calibration = [] 
    bias = (0.0, 0.0, 0.0)
    calibrated = False

    smooth_x = 0.0       
    smooth_y = 0.0
    leftover_x = 0.0     
    leftover_y = 0.0
    last_click_time = 0.0
    last_click_dir = 0   
    click_armed = True   

    try:
        while True:
            data, addr = sock.recvfrom(1024)
            pkt = parse(data)
            if pkt is None:
                continue

            seq, t, gx, gy, gz = pkt
            if seq <= last_seq and last_seq - seq < RESTART_GAP:
                continue  
            last_seq = seq

            
            if not calibrated:
                calibration.append((gx, gy, gz))
                if len(calibration) >= CALIBRATION_SAMPLES:
                    n = len(calibration)
                    bias = (sum(s[0] for s in calibration) / n,
                            sum(s[1] for s in calibration) / n,
                            sum(s[2] for s in calibration) / n)
                    calibrated = True
                    print("Calibration done. Head-mouse is active!")
                continue

            
            gx -= bias[0]
            gy -= bias[1]
            gz -= bias[2]

           
            tilt = -gy if INVERT_TILT else gy
            now = time.time()
            if abs(tilt) < CLICK_THRESHOLD * 0.5:
                click_armed = True  

            direction = 1 if tilt > CLICK_THRESHOLD else -1 if tilt < -CLICK_THRESHOLD else 0
            if direction != 0 and click_armed:
                wait = CLICK_COOLDOWN if direction == last_click_dir else RETURN_LOCKOUT
                if now - last_click_time >= wait:
                    mouse.click(Button.left if direction > 0 else Button.right)
                    print("Left click (tilted left)" if direction > 0 else "Right click (tilted right)")
                    last_click_time = now
                    last_click_dir = direction
                    click_armed = False
                    continue

            
            move_x = deadzone(-gz if INVERT_X else gz) * SENSITIVITY
            move_y = deadzone(-gx if INVERT_Y else gx) * SENSITIVITY

            
            smooth_x = SMOOTHING * move_x + (1 - SMOOTHING) * smooth_x
            smooth_y = SMOOTHING * move_y + (1 - SMOOTHING) * smooth_y

            
            leftover_x += smooth_x
            leftover_y += smooth_y
            step_x = int(leftover_x)
            step_y = int(leftover_y)
            leftover_x -= step_x
            leftover_y -= step_y

            if step_x != 0 or step_y != 0:
                mouse.move(step_x, step_y)

            if seq % PRINT_EVERY == 0:
                print(f"{seq:7d}  gx={gx:+.2f}  gy={gy:+.2f}  gz={gz:+.2f}  ->  dx={step_x:+d} dy={step_y:+d}")
    except KeyboardInterrupt:
        print("Stopped.")


if __name__ == "__main__":
    main()

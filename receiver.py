import socket
import time

from pynput.mouse import Controller, Button

mouse = Controller()

PORT = 5005
SENSITIVITY = 30.0

INVERT_X = True
INVERT_Y = True
INVERT_TILT = True

CLICK_THRESHOLD = 1.3
CLICK_COOLDOWN = 0.6


def parse(data):
    try:
        parts = data.decode().strip().split(",")
        if len(parts) != 5:
            return None
        gx = float(parts[2])
        gy = float(parts[3])
        gz = float(parts[4])
        return gx, gy, gz
    except (UnicodeDecodeError, ValueError):
        return None


def main():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(("0.0.0.0", PORT))
    print(f"Listening on UDP port {PORT}...")

    last_click_time = 0.0

    while True:
        data, _ = sock.recvfrom(1024)
        pkt = parse(data)
        if pkt is None:
            continue

        gx, gy, gz = pkt

        tilt = -gz if INVERT_TILT else gz
        now = time.time()
        if now - last_click_time >= CLICK_COOLDOWN:
            if tilt > CLICK_THRESHOLD:
                mouse.click(Button.left)
                last_click_time = now
                continue
            elif tilt < -CLICK_THRESHOLD:
                mouse.click(Button.right)
                last_click_time = now
                continue

        move_x = (-gy if INVERT_X else gy) * SENSITIVITY
        move_y = (-gx if INVERT_Y else gx) * SENSITIVITY

        mouse.move(int(move_x), int(move_y))

if __name__ == "__main__":
    main()

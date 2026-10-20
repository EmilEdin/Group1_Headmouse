import socket
import sys
import time

from sense_hat import SenseHat

sense = SenseHat()
sense.set_imu_config(False, True, True)

LAPTOP_IP = sys.argv[1]
PORT = 5005
RATE_HZ = 100

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
start = time.time()
seq = 0

print(f"Sending gyro data to {LAPTOP_IP}:{PORT}...")

while True:
    t = time.time() - start

    gyro = sense.get_gyroscope_raw()
    gx = gyro["x"]
    gy = gyro["y"]
    gz = gyro["z"]

    msg = f"{seq},{t:.4f},{gx:.4f},{gy:.4f},{gz:.4f}"
    sock.sendto(msg.encode(), (LAPTOP_IP, PORT))

    seq += 1
    time.sleep(1 / RATE_HZ)

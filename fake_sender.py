import math
import socket
import time

TARGET = ("127.0.0.1", 5005)   # later: the laptop's IP, e.g. ("172.20.10.3", 5005)
RATE_HZ = 100

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
start = time.time()
seq = 0

while True:
    t = time.time() - start
    gx, gy, gz = 0.5 * math.sin(t), 0.5 * math.cos(t), 0.0   # fake rad/s
    msg = f"{seq},{t:.4f},{gx:.4f},{gy:.4f},{gz:.4f}"
    sock.sendto(msg.encode(), TARGET)
    seq += 1
    time.sleep(1 / RATE_HZ)

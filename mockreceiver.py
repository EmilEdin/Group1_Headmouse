import csv
import socket
import time

PORT = 5005
FIELDS = 5            # seq, t, gx, gy, gz
RESTART_GAP = 100     # a seq drop larger than this means the Pi sender restarted
PRINT_EVERY = 10      # print every Nth packet to keep the terminal readable


def parse(data):
    """Return (seq, t, gx, gy, gz), or None if the packet is invalid."""
    try:
        parts = data.decode().strip().split(",")
        if len(parts) != FIELDS:
            return None
        seq = int(parts[0])
        t, gx, gy, gz = map(float, parts[1:])
        return seq, t, gx, gy, gz
    except (UnicodeDecodeError, ValueError):
        return None


def main():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    """
    socket.AF_INET sets the address family to IPv4, so addresses look like 172.20.10.3
    socket.SOCK_DGRAM sets the socket type to datagram, which means UDP
    """
    sock.bind(("0.0.0.0", PORT))
    print(f"Listening on UDP port {PORT}... (Ctrl+C to stop)")

    last_seq = -1
    with open("gyro_log.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["recv_time", "seq", "t", "gx", "gy", "gz"])
        try:
            while True:
                data, addr = sock.recvfrom(1024)
                pkt = parse(data)
                if pkt is None:
                    print(f"Invalid packet from {addr}: {data!r}")
                    continue

                seq, t, gx, gy, gz = pkt
                if seq <= last_seq and last_seq - seq < RESTART_GAP:
                    continue  # old or duplicate packet
                if last_seq >= 0 and seq > last_seq + 1:
                    print(f"Lost {seq - last_seq - 1} packet(s)")
                last_seq = seq

                writer.writerow([time.time(), seq, t, gx, gy, gz])
                if seq % PRINT_EVERY == 0:
                    print(f"{seq:7d}  gx={gx:+.3f}  gy={gy:+.3f}  gz={gz:+.3f}")
        except KeyboardInterrupt:
            print("Stopped. Data saved to gyro_log.csv")


if __name__ == "__main__":
    main()
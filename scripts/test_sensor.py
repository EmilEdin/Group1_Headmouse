#!/usr/bin/env python3
"""
Test script to read and display telemetry from the Sense HAT IMU (Pitch, Roll, Yaw).
Falls back to a simulated mock stream if running on hardware without the Sense HAT.
"""

import sys
import time
import math

try:
    from sense_hat import SenseHat
    sense = SenseHat()
    is_mock = False
    print("[INFO] Sense HAT hardware detected.")
except (ImportError, OSError):
    is_mock = True
    print("[WARN] Sense HAT hardware not found. Running in SIMULATED test mode.\n")

def get_telemetry(step: int) -> dict:
    """Returns orientation dict containing pitch, roll, and yaw."""
    if not is_mock:
        # Fetches degrees (0.0 to 360.0) from the Sense HAT IMU
        return sense.get_orientation()
    else:
        # Generate synthetic sine-wave tilt angles for local testing
        t = step * 0.1
        return {
            "pitch": (math.sin(t) * 25.0) % 360.0,
            "roll": (math.cos(t) * 25.0) % 360.0,
            "yaw": (t * 5.0) % 360.0
        }

def main():
    print("==========================================")
    print(" Sense HAT IMU Telemetry Diagnostic Tool  ")
    print(" Press Ctrl+C to exit                     ")
    print("==========================================\n")
    print(f"{'Sample':<8} | {'Pitch (deg)':<14} | {'Roll (deg)':<14} | {'Yaw (deg)':<14}")
    print("-" * 58)

    sample_count = 0
    try:
        while True:
            orientation = get_telemetry(sample_count)
            pitch = orientation["pitch"]
            roll = orientation["roll"]
            yaw = orientation["yaw"]

            # Format angles between -180 and +180 for standard head-tilt visualization
            norm_pitch = pitch - 360.0 if pitch > 180.0 else pitch
            norm_roll = roll - 360.0 if roll > 180.0 else roll

            print(
                f"{sample_count:<8} | "
                f"{pitch:6.2f}° ({norm_pitch:+6.2f}°) | "
                f"{roll:6.2f}° ({norm_roll:+6.2f}°) | "
                f"{yaw:6.2f}°",
                end="\r"
            )
            sys.stdout.flush()

            sample_count += 1
            time.sleep(0.05)  # 20 Hz output

    except KeyboardInterrupt:
        print("\n\n[INFO] Diagnostic session terminated cleanly.")

if __name__ == "__main__":
    main()
# Group 1 - Head-Mouse Setup Guide

This guide walks through flashing the Raspberry Pi OS, setting up the hardware, installing dependencies, and verifying telemetry from the Sense HAT.

---

## 1. Hardware Assembly
1. Align the 40-pin header of the **Sense HAT** with the Raspberry Pi GPIO pins.
2. Firmly press down until seated flat against the standoffs.
3. Connect power via USB-C.

---

## 2. Flashing Raspberry Pi OS
1. Download and launch **Raspberry Pi Imager** on your computer.
2. **Choose Device:** Raspberry Pi 4 (or Pi 3 / Pi 5 depending on model).
3. **Choose OS:** Raspberry Pi OS (64-bit with Desktop).
4. **Choose Storage:** Select your microSD card.
5. Click **Edit Settings** (gear icon) to preconfigure:
   - Hostname: `headmouse`
   - Username & Password
   - Wi-Fi network credentials
   - Enable SSH (Password authentication)
6. Click **Write** and verify the flash.
7. Insert the SD card into the Pi and power it on.

---

## 3. Dependency Installation
Clone the repository and run the automated setup script:

```bash
git clone [https://github.com/EmilEdin/Group1_Headmouse.git](https://github.com/EmilEdin/Group1_Headmouse.git)
cd Group1_Headmouse
chmod +x setup.sh
./setup.sh
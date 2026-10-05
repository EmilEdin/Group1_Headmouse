# Sense HAT Installation

> Source: [Raspberry Pi documentation on GitHub](https://github.com/raspberrypi/documentation/blob/master/documentation/asciidoc/accessories/sense-hat/software.adoc)

## Requirements

The Sense HAT needs:

- an up-to-date kernel
- [I2C](https://en.wikipedia.org/wiki/I%C2%B2C) enabled on the Raspberry Pi
- a few dependencies

> **Note:** Run these commands **on the Raspberry Pi** (e.g. over SSH), not on your own computer.

## 1. Update the system

```bash
sudo apt update && sudo apt full-upgrade
```

## 2. Install the `sense-hat` package

This updates the kernel, enables I2C and installs the dependencies:

```bash
sudo apt install sense-hat
```

## 3. Reboot

Rebooting enables I2C and loads the new kernel (if it changed):

```bash
sudo reboot
```

# Sense HAT Calibration

(These notes are taken from the webpage https://www.raspberrypi.com/documentation/accessories/sense-hat.html on the 5th of October)

## 1. Install and launch

Connect to the Raspberry PI (with an example IP): 
```bash 
ssh pi@192.168.1.42
```

Install the required software and start the calibration program:

```bash
sudo apt update
sudo apt install octave -y
cd
cp /usr/share/librtimulib-utils/RTEllipsoidFit ./ -a
cd RTEllipsoidFit
RTIMULibCal
```

The program shows this menu:

```
Options are:

  m - calibrate magnetometer with min/max
  e - calibrate magnetometer with ellipsoid (do min/max first)
  a - calibrate accelerometers
  x - exit

Enter option:
```

## 2. Magnetometer min/max calibration

Press **`m`**. This message appears — press any key to start:

```
Magnetometer min/max calibration
-------------------------------
Waggle the IMU chip around, ensuring that all six axes
(+x, -x, +y, -y and +z, -z) go through their extrema.
When all extrema have been achieved, enter 's' to save, 'r' to reset
or 'x' to abort and discard the data.

Press any key to start...
```

Output like this will scroll up the screen:

```
Min x:  51.60  min y:  69.39  min z:  65.91
Max x:  53.15  max y:  70.97  max z:  67.97
```

> **Tip:** Watch the two bottom lines — they are the most recent measurements.

### Move the device

- Pick up the Raspberry Pi + Sense HAT and move it in every way you can.
- Unplug non-essential cables to avoid clutter.
- Aim for a full circle in each of **pitch**, **roll** and **yaw**.
- Be careful not to eject the SD card.
- Keep going for a few minutes, until the numbers stop changing.

### Save and exit

Press **`s`**, then **`x`**. Running `ls` should now show a new `RTIMULib.ini` file.

## 3. Ellipsoid fit (optional)

Repeat the steps above, but press **`e`** instead of `m`. Do the min/max calibration first.

## 4. Install the calibration file

Copy the result to `/etc/` and remove the local copy:

```bash
rm ~/.config/sense_hat/RTIMULib.ini
sudo cp RTIMULib.ini /etc
```



# Delta Robot 

Product page: https://www.igus.eu/product/20433?artNr=DLE-DR-0005

The [iRC User Manual](https://www.igus.eu/ContentData/Products/Downloads/iRC_R13_UserGuide_en.pdf) has the Modbus documentation. This manual can be found in the Downloads tab or the product page.

The [Robot Software](https://www.igus.eu/info/robot-software) page also has interesting documentation. Here one can find information on the [Modbus Server](https://wiki.cpr-robots.com/index.php/Modbus_Server)


## Connection using Ethernet

Robot uses linux based system for its main computer with IP 192.168.3.11/24
PC connecting to it must have an IP address in the range of 192.168.3.0-255/24

An ethernet cable can be connected between the robot and the PC, or to connect the robot to a LAN.

The robot linux system can be accessed through SSH with username: robot and password: robot

[Read more](https://cpr-robots.com/download/TinyCtrl/Filezilla_Putty_EmbCtrlAccess.pdf)

## Start Up sequence

Steps:
- connect
- reset
- activate
- reference all
- reset 
- activate

## ModbusTCP

The modbus server of the robot is implemented in the TinyCtrl robot control. Versions 12 and 13 of the modbus require license. Without a license the modbusTPC server can oly be used for 30 mins. Robot must be restarted to get another 30 mins. Verion 14 and after can be used without a license. 

> NOTE: Check what version of the modbusTCP implementation the robot is using!!!!!

Read more [here](https://wiki.cpr-robots.com/index.php/Modbus_Server) and also in the User Manual

### Test connection

To test whether the Modbus connection is successful the input registers on addresses 0-3 can be read: These contain the TinyCtrl version and mapping version, e.g. 980, 12, 20, 1.

### Moving using modbusTCP

The approach for sending a position and starting a motion is the same for all types:

- Write the position values to the holding registers
- Write the motion velocity to holding register 180
- Write a rising edge (0, then 1) to the coil to start the motion

The register and coil addresses depend on the motion type, you will find them in the user manual.

Read more (here)[https://wiki.cpr-robots.com/index.php/Moving_Robots_via_Modbus]

# Gripper

Two servos are used to control the gripper. One rotates the gripper along the z axis. Another closes and opens the grip.

An ESP32 board is used to control the servos. The RberryPi and the ESP32 communicate over serial-usb. The provided Arduino code runs on the ESP32.

There is a way to control these two servos using the RberryPi:
- [Using PWM directly](https://projects.raspberrypi.org/en/projects/grandpa-scarer/3). 
- [RaspberryPi python package](https://www.digikey.com/en/maker/tutorials/2021/how-to-control-servo-motors-with-a-raspberry-pi)

# RaspberryPi

## Python
Installed python3.12.3 as alternate install and made it the default for python3 command
Read more [here](https://raspberrytips.com/install-latest-python-raspberry-pi/)

Installed packages:
- pyModbusTCP
- numpy


## IP Address

Assigned a static IP address to ethernet port as:
```bash
sudo ifconfig eth0 192.168.3.1/24
```

This allows the Delta robot to be connected directly to the pi instead of the Technikum WLAN. 

The pi's IP address must be in the subnet of 192.168.3.0-255/24
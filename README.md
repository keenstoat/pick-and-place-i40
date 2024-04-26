


# Delta Robot 

Product page: https://www.igus.eu/product/20433?artNr=DLE-DR-0005

The [iRC User Manual](https://www.igus.eu/ContentData/Products/Downloads/iRC_R13_UserGuide_en.pdf) has the Modbus documentation. This manual can be found in the Downloads tab or the product page.

The [Robot Software](https://www.igus.eu/info/robot-software) page also has interesting documentation. Here one can find information on the [Modbus Server](https://wiki.cpr-robots.com/index.php/Modbus_Server)


## Connecting to the robot using Ethernet

The robot uses linux based system for its main computer with IP `192.168.3.11/24`

A PC connecting to the robot must have an IP address in the `192.168.3.0/24` network. 

> We use `192.168.3.1/24`
>
> Remember .0 and .255 cannot be used (they are the network and broadcast addresses)

The robot can be connected:
- Directly to a PC
- To a LAN

In the Technikum, two configurations work:
- Connect the robot to an ethernet port (usnig a network cable) and then connect the PC to the Technikum's WiFi.
- Connect the robot directly to the PC's ethernet port.

The robot linux system can be accessed through SSH with:
- username: `robot` 
- password: `robot`

Read more [here](https://cpr-robots.com/download/TinyCtrl/Filezilla_Putty_EmbCtrlAccess.pdf)

## Robot start Up sequence

Steps:
- connect
- reset
- activate
- reference all
- reset 
- activate

## ModbusTCP

The modbus server of the robot is implemented in the TinyCtrl robot control. Versions 12 and 13 of the modbus require license. Without a license the modbusTPC server can only be used for 30 mins. The robot must be restarted to get another 30 mins to play. Verion 14 and after can be used without a license. 

> NOTE: Check what version of the modbusTCP implementation the robot is using!!!!!

> Read more [here](https://wiki.cpr-robots.com/index.php/Modbus_Server) and also in the User Manual

### Test connection

To test whether the Modbus connection is successful the input registers on addresses 0-3 can be read: These contain the TinyCtrl version and mapping version, e.g. 980, 12, 20, 1.

### Moving the robot using modbusTCP

The approach for sending a position and starting a motion is the same for all types:

- Write the position values to the holding registers
- Write the motion velocity to holding register 180
- Write a rising edge (0 then 1) to the coil to start the motion

The register and coil addresses depend on the motion type, you will find them in the user manual.

> Read more [here](https://wiki.cpr-robots.com/index.php/Moving_Robots_via_Modbus)

#### Range of movement

The range of movement for the robot is depicted [here](https://www.igus.eu/ContentData/Products/Downloads/Delta%20Roboter%20DLE-DR-0050_DINA5_v2.pdf)

# Gripper

The gripper is part of the delta robot.

Two servos are used to control the gripper. One rotates the gripper along the z axis. Another closes and opens the grip.

An ESP32 board is used to control the servos. The RberryPi and the ESP32 communicate over serial-usb. The provided Arduino code runs on the ESP32.

There is a way to control these two servos using the RberryPi:
- [Using PWM directly](https://projects.raspberrypi.org/en/projects/grandpa-scarer/3). 
- [RaspberryPi python package](https://www.digikey.com/en/maker/tutorials/2021/how-to-control-servo-motors-with-a-raspberry-pi)

# RaspberryPi

A RaspberryPi is used as PC to connect with the robot. 

The code provided by [YAlsaady Delta Robot GitHub Repo](https://github.com/YAlsaady/IGUS_Delta_Robot) works at first glance. A deeper dive reveals some inconsistencies such as:
- waiting for robot to move does not work as expected
- python `match` statement is used but the python version in the pi does not support this.

## IP Address

As stated previously in [Connecting to the robot using Ethernet](./README.md#connecting-to-the-robot-using-ethernet), a static IP address has been assigned to the ethernet port  as:
```bash
sudo ifconfig eth0 192.168.3.1/24
```

This allows the Delta robot to be connected directly to the pi instead of the Technikum LAN. The robot is no longer accessible in the WLAN but it no longer has to be connected to a wall socket!

## Python Runtime

The installed python version found in the pi is 3.9.

I've installed `python3.12.3` as alternate install.

These are the steps to install it:
```bash
# install ssl libs and other required packages
sudo apt install -y build-essential zlib1g-dev libncurses5-dev libgdbm-dev libnss3-dev libssl-dev libreadline-dev libffi-dev wget cmake

# download python tarball
wget https://www.python.org/ftp/python/3.12.3/Python-3.12.3.tgz

# un tar it
tar -zxvf Python-3.12.3.tgz 

# configure installation
cd Python-3.12.3/
./configure --enable-optimizations

# install along side existing python
sudo make altinstall
```

The new python should be installed under `/usr/local/bin`

> Read more [here](https://raspberrytips.com/install-latest-python-raspberry-pi/)

After installation, create a symlink to access `python3.12` as `python312`:
```bash
cd /usr/local/bin
ln -s python3.12 python312
```

### Python virtual environment

A virtual env allows you to encapsulate your python development and runtime environment. 

This is useful when several persons are working on the same host or you are trying out different versions of the same packages.

Create a virtual env named `venv312` in your home directory as:
```bash
cd ~
python312 -m venv venv312
```

To have the venv activated when the user logs in, add this line in the `~/.bashrc` file: 
```
source ~/venv312/bin/activate
```

Now install the following packages using pip (versions are at the time of install)
- numpy==1.26.4
- pip==24.0
- pyModbusTCP==0.2.1
- setuptools==69.5.1
- wheel==0.43.0

> Numpy requires setuptools and wheel, and it is only required for the `linspace` function. TODO check if this function can be custom.

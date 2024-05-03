# RaspberryPi

A RaspberryPi is used as PC to connect with the robot. 

The code provided by [YAlsaady Delta Robot GitHub Repo](https://github.com/YAlsaady/IGUS_Delta_Robot) works at first glance. A deeper dive reveals some inconsistencies such as:
- waiting for robot to move does not work as expected
- python `match` statement is used but the python version in the pi does not support this.

## Create user

Since I don't know the password for the `pi` user and I have access to the desktop and the `pi` user has passwordless sudo then we can create our own user.

```bash
# create user and follow the instructions
sudo adduser charles

# create group wheel
sudo groupadd wheel

# add charles user to group wheel
sudo adduser charles wheel
```

Now add passwordless sudo permissions to group wheel. Add the following in the sudoers file. Edit the sudoers file with `visudo`:
```
%wheel    ALL = (ALL) NOPASSWD: ALL
```

## IP Address

As stated previously in [Connecting to the robot using Ethernet](./README.md#connecting-to-the-robot-using-ethernet), a static IP address must be assigned to the ethernet port of the PC connecting to the robot. 

From the RaspberriPi run:
```bash
sudo ifconfig eth0 192.168.3.1/24
```

Or from your local run:

```bash
ssh charles@192.168.158.89 'sudo ifconfig eth0 192.168.3.1/24'
```


This allows the Delta robot to be connected directly to the pi instead of the Technikum LAN. The robot is no longer accessible in the WLAN but it no longer has to be connected to a wall socket!

## Using an SSH Tunnel to connect from your localhost to the Delta robot

A RaspberryPi is used as PC to connect to the robot.

Instead of connecting to the RaspberryPi and cloning the repo and working in it a tunnel can be used.

The following command forwards your localhost 5020 port to the Delta robot's 502 port (modbus port) using the RaspberryPi as a jump server.

```bash

# genral form is: ssh -N -L localport:robotIpAddress:modbusPort username@raspberryPiIpAddress
ssh -N -L 5020:192.168.3.11:502 charles@192.168.158.89 
```

Now, use `localhost` and `5020` as host and port in your delta robot's modbus address in your python code

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



# Gripper

The gripper is part of the delta robot.

Two servos are used to control the gripper. One rotates the gripper along the z axis. Another closes and opens the grip.

An ESP32 board is used to control the servos. The RberryPi and the ESP32 communicate over serial-usb. The provided Arduino code runs on the ESP32.

There is a way to control these two servos using the RberryPi:
- [Using PWM directly](https://projects.raspberrypi.org/en/projects/grandpa-scarer/3). 
- [RaspberryPi python package](https://www.digikey.com/en/maker/tutorials/2021/how-to-control-servo-motors-with-a-raspberry-pi)


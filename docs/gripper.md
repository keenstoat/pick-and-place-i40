

# Gripper

The gripper is part of the delta robot.

Two servos are used to control the gripper. One rotates the gripper along the z axis. Another closes and opens the grip.

An ESP32 board is used to control the servos. The RberryPi and the ESP32 communicate over serial-usb. The provided Arduino code runs on the ESP32.

There is a way to control these two servos using the RberryPi:
- [Using PWM directly](https://projects.raspberrypi.org/en/projects/grandpa-scarer/3). 
- [RaspberryPi python package](https://www.digikey.com/en/maker/tutorials/2021/how-to-control-servo-motors-with-a-raspberry-pi)


# Arduino

The mc code reads a string from the Serial interface and parses it as JSON. 



```
{"action": "status"}
{"action": "open", "value": 0, "relative": true}
{"action": "rotate", "value": 0, "relative": true}
```


# Refs

https://randomnerdtutorials.com/esp32-servo-motor-web-server-arduino-ide/

https://randomnerdtutorials.com/installing-the-esp32-board-in-arduino-ide-windows-instructions/

https://arduino.stackexchange.com/questions/84328/getting-all-data-of-my-json-object-from-serial-read-at-once

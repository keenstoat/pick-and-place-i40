# Integration App for Pick and Place Module

## Gripper ESP32 firmware

This must be loaded to the ESP32 board to control the gripper.

The gripper is broken and no longer opens and closes. It does not rotate correctly.

## App

The app is a python application that connects to the Delta Robot through ModbusTCP, to the ESP32 through a serial interface (serial over USB). 

The app implements an HTTP REST API to expose some basic functions to control the Delta Robot and the gripper. 

The FAST server asset connection consumes the exposed function endpoints to implement communication with an OPC UA server.

## Installation with Docker

The app can be used as is with python. The installation just needs the packages defined in the requirements.txt file. 

For easier use and because it makes sense with the rest of the project, the app can be installed using docker. Just need to build the image and run it in the Raspberry Pi. This is made even easier with the docker compose file provided.

Make sure the `/dev/ttyUSB0` file has read and write permissions for the user running the docker container. (Hint: add the user to the dialout group)

## Creating the Docker image

The docker image can be built in your local linux distro or in the Raspberry Pi.
#!/usr/bin/env python3

from serial import Serial
from time import time
from sys import argv, exit
from json import dumps, loads


class Gripper:

    MAX_OPENING_MM = 64

    def __init__(self, port:str="/dev/ttyUSB0", baudrate:int=115200, timeout:int=1):
        
        self.serial = Serial(port, baudrate, timeout=timeout)

    @property
    def is_connected(self):
        return self.serial.is_open

    def wait_for_response(self, max_delay_ms=2000):

        now = time()
        timeout = now + max_delay_ms/1000
        while not(result := self.serial.readall()): 
            if time() > timeout:
                return None
        return loads(result.decode()) if result else None
    
    def get_status(self):
        if not self.is_connected:
            return
        
        commandJson = dumps({"action": "status"})
        self.serial.write(commandJson.encode())

        return self.wait_for_response()

    def get_openning(self):
        return self.get_status()["opening"]

    def get_rotation(self):
        return self.get_status()["rotation"]

    def open_percent(self, percent:int, relative:bool=False):
        if not self.is_connected:
            return
        
        commandJson = dumps({"action": "open", "value": percent, "relative": relative})
        self.serial.write(commandJson.encode())

        return self.wait_for_response()
    
    def open(self, millis:int, relative:bool=False):
        if not self.is_connected:
            return
        
        value = millis * 100 / Gripper.MAX_OPENING_MM

        commandJson = dumps({"action": "open", "value": value, "relative": relative})
        self.serial.write(commandJson.encode())

        return self.wait_for_response()

    def rotate(self, degrees:int, relative:bool=False):
        if not self.is_connected:
            return
        
        commandJson = dumps({"action": "rotate", "value": degrees, "relative": relative})
        self.serial.write(commandJson.encode())

        return self.wait_for_response()

    def config(self, rotateMaxDelayMs=None, openMaxDelayMs=None):
        if not self.is_connected:
            return
        
        payload = {"action": "config"}

        if rotateMaxDelayMs is not None:
            payload["rotateMaxDelayMs"] = rotateMaxDelayMs

        if openMaxDelayMs is not None:
            payload["openMaxDelayMs"] = openMaxDelayMs


        commandJson = dumps(payload)
        self.serial.write(commandJson.encode())

        return self.wait_for_response()

if __name__ == "__main__":

    argv.pop(0)
    if not argv:
        exit(1)

    action = argv.pop(0)
    if argv:
        value = int(argv.pop(0))
        
    rel = True if argv and argv.pop(0)=="true" else False
    g = Gripper()

    if action == "open": print(g.open_percent(value, rel))
    if action == "mm": print(g.open(value, rel))
    if action == "rotate": print(g.rotate(value, rel))
    if action == "status": print(g.get_status())
    if action == "opening": print(g.get_openning())
    if action == "rotation": print(g.get_rotation())

    if action == "rotateMaxDelayMs": print(g.config(rotateMaxDelayMs=value))
    if action == "openMaxDelayMs": print(g.config(openMaxDelayMs=value))
    
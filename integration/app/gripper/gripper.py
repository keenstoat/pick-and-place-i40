#!/usr/bin/env python3

from serial import Serial
from time import time
from sys import argv, exit
from json import dumps, loads
from threading import Semaphore


class Gripper:

    MAX_OPENING_MM = 64

    def __init__(self, port:str="/dev/ttyUSB0", baudrate:int=115200, timeout:int=1):
        
        self.serial = Serial(port, baudrate, timeout=timeout)
        self.sem = Semaphore()

    @property
    def is_connected(self):
        return self.serial.is_open

    def send_command(self, payload:dict):

        command_json = dumps(payload)
        self.sem.acquire()
        self.serial.write(command_json.encode())
        response = self.wait_for_response()
        self.sem.release()
        return response

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

        return self.send_command({"action": "status"})

    def get_openning(self):
        return self.get_status()["opening"]

    def get_rotation(self):
        return self.get_status()["rotation"]

    def open_percent(self, percent:int, relative:bool=False):
        if not self.is_connected:
            return
        
        return self.send_command({"action": "open", "value": percent, "relative": relative})
    
    def open(self, millis:int, relative:bool=False):
        if not self.is_connected:
            return
        
        value = millis * 100 / Gripper.MAX_OPENING_MM
        return self.send_command({"action": "open", "value": value, "relative": relative})

    def rotate(self, degrees:int, relative:bool=False):
        if not self.is_connected:
            return
        
        return self.send_command({"action": "rotate", "value": degrees, "relative": relative})

    def config(self, rotateMaxDelayMs=None, openMaxDelayMs=None):
        if not self.is_connected:
            return
        
        payload = {"action": "config"}

        if rotateMaxDelayMs is not None:
            payload["rotateMaxDelayMs"] = rotateMaxDelayMs

        if openMaxDelayMs is not None:
            payload["openMaxDelayMs"] = openMaxDelayMs

        return self.send_command(payload)

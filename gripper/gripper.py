#!/usr/bin/env python3

from serial import Serial
from time import time
from sys import argv, exit


class Gripper:
    is_connected: bool = False
    orientation = 0
    opening = 0
    last_control_time = 0

    def __init__(self, port:str = "/dev/ttyUSB0", baudrate:int = 115200, timeout:int = 1, movement_time: float = 1):
        """
        Initialize the Gripper instance.

        :param port: The serial port for communication (default is "/dev/ttyUSB0").
        :type port: str
        :param baudrate: The baud rate for serial communication (default is 115200).
        :type baudrate: int
        :param timeout: The timeout for serial communication (default is 1 second).
        :type timeout: int
        :param movement_time: The maximum movement time in seconds (default is 1 second).
        :type movement_time: float
        """
        self.serial = Serial(port, baudrate, timeout=timeout)
        self.orientation = 90
        self.opening = 100
        self.open_min = 90
        self.open_max = 180
        self.orient_min = 30
        self.orient_max = 150
        self.table_hight = 0

        self.movement_time = movement_time
        self.table_movement_time = 0
        self.last_control_time = time()


    @property
    def is_connected(self):
        return self.serial.is_open
    
    def control(self, opening:int, orientation:int=None, table_hight:int=0):

        if not self.is_connected:
            return
        
        if not (0 <= opening <= 100):
            return False  # Opening value out of range
        
        if orientation is not None and not (0 <= orientation <= 180):
            return False  # Orientation value out of range

        if self.opening == opening and self.orientation == orientation and self.table_hight == table_hight:
            return True

        if orientation is None:
            orientation = self.orientation

        if self.opening == opening and self.orientation == orientation:
            self.last_control_time = time()
        else:
            self.last_control_time = time() + self.movement_time

        self.opening = opening
        self.orientation = orientation

        table_hight = int(table_hight)
        self.table_hight = table_hight

        opening = int((opening * (self.open_max - self.open_min) / 100) + self.open_min)
        orientation = 180 - int(
            (orientation * (self.orient_max - self.orient_min) / 180) + self.orient_min
        )
        if table_hight == 2:
            table_hight = -1
        pos = f"{opening} {orientation} {table_hight}\n"
        print(pos)

        self.serial.write(pos.encode())

    def is_moving(self) -> bool:
        """
        Check if the gripper is still moving after the last control operation.

        This method calculates the time since the last control operation and compares it with the maximum movement time.
        If the time since the last control operation is less than the maximum movement time, it returns True,
        indicating that the gripper is still moving. Otherwise, it returns False.

        Additionally, if the delta robot is connected, it sets a global signal to indicate the gripper's movement state.

        :return: True if the gripper is still moving, False otherwise.
        :rtype: bool
        """
        time_since_last_control = time() - self.last_control_time
        state = time_since_last_control < self.movement_time
        if self.delta.is_connected:
            self.delta.set_globale_signal(7, state)
        return state

    def open(self):
        if not self.is_connected:
            return
        self.control(0)

    def close(self):
        if not self.is_connected:
            return
        self.control(100)

    def rotate(self, degrees:int):
        if not self.is_connected:
            return
        
        if not (0 <= degrees <= 180):
            return False  # Orientation value out of range

        self.control(self.opening, self.orientation)

if __name__ == "__main__":
    argv.pop(0)
    if not argv:
        exit(1)

    degrees = int(argv[0])

    Gripper().rotate(degrees)





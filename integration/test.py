#!/usr/bin/env python3

from delta_robot.delta_robot import DeltaRobot
from gripper.gripper import Gripper
from time import sleep

import paramiko


class Module:
    ROBOT_BASE_TO_END_EFFECTOR_BASE_INITIAL_DISTANCE = 290 # mm
    ROBOT_Z_RANGE = 300 # mm
    GRIPPER_HEIGHT = 140 # mm
    
    def __init__(self, table_distance_from_robot_base, delta_robot_ip_addr, delta_robot_port):

        # self.gripper = Gripper()
        self.robot = DeltaRobot(delta_robot_ip_addr, port=delta_robot_port)
        assert self.robot.is_connected, "DeltaRobot is not connected"

        print("Has General Error       : ", self.robot.has_module_error())
        print("Has Kinemat Error       : ", self.robot.has_kinematics_error())
        print()
        print("Module Error List   : ", self.robot.get_module_error_list())
        print("Kino Error List     : ", self.robot.get_kinematics_error_list())
        print("Kino error single   : ", self.robot.get_kinematics_error())
        print("Info or error short : ", self.robot.get_info_or_message())
        print()

        if not self.robot.is_referenced():
            print("Robot NOT referenced. Resetting now.")
            self.robot.reset()
            print("Enabling motors now..")
            self.robot.enable()
            print("Referencing now..")
            if not self.robot.reference():
                print("Coult NOT reference self.robot. Try again")
                return
        print("Robot is referenced!")

        self.robot.enable()
        self.robot.set_override_velocity(100)
        self.robot.set_velocity(400)
        self.robot.move_cartesian(x=0, y=0, z=self.ROBOT_Z_RANGE)
        self.robot_lowest_position = self.get_robot_lowest_position(table_distance_from_robot_base)

        self.open_mm(0)
        self.rotate(90)

    def get_robot_lowest_position(self, table_distance_from_robot_base):
        self.table_distance_from_robot_base = table_distance_from_robot_base

        return self.ROBOT_BASE_TO_END_EFFECTOR_BASE_INITIAL_DISTANCE + self.ROBOT_Z_RANGE \
            - self.table_distance_from_robot_base + self.GRIPPER_HEIGHT

    # TODO this mocks the actual gripper code
    def open_mm(self, value):
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect("192.168.158.89", username="charles", password="asdf123")
        ssh.exec_command(f"sudo ./gripper.py mm {value}")
        sleep(2)

    # TODO this mocks the actual gripper code
    def rotate(self, value):
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect("192.168.158.89", username="charles", password="asdf123")
        ssh.exec_command(f"sudo ./gripper.py rotate {value}")

    def step(self, msg):
        # return
        print(msg)

    def pick(self, x, y, object_width, object_height):
        
        z_ini = self.robot_lowest_position + object_height + 10 # mm

        self.step("position above object")
        self.robot.move_cartesian(x=x, y=y, z=z_ini)
        
        self.step("open gripper...")
        # self.gripper.open_mm(object_width + 10)
        self.open_mm(object_width + 10)

        self.step("position to grab object")
        self.robot.move_cartesian(z=self.robot_lowest_position + object_height//2 - 10)
        
        self.step("close gripper...")
        # self.gripper.open_mm(object_width)
        self.open_mm(object_width-5)

        self.step("pick up object")
        self.robot.move_cartesian(x=0, y=0, z=self.ROBOT_Z_RANGE)
        
    def place(self, x, y, object_width, object_height):
        
        z_ini = self.robot_lowest_position + object_height + 10 # mm

        self.step("position to place object")
        self.robot.move_cartesian(x=x, y=y, z=self.robot_lowest_position + object_height//2 - 10)
        
        self.step("open gripper...")
        # self.gripper.open_mm(object_width + 10)
        self.open_mm(object_width + 10)

        self.step("position above object")
        self.robot.move_cartesian(z=z_ini)

        self.step("return to base position")
        self.robot.move_cartesian(x=0, y=0, z=self.ROBOT_Z_RANGE)
        
        self.step("close gripper...")
        # self.gripper.open_mm(object_width)
        self.open_mm(0)

        
        
        



# _delta_robot_ip_addr = "192.168.3.11"
_delta_robot_ip_addr = "localhost"
_delta_robot_port = 5020
_table_distance = 600
module = Module(_table_distance, _delta_robot_ip_addr, _delta_robot_port)


_w = 25
_h = 100

_x = 0
_y = -100
module.pick(_x, _y, _w, _h)

_x = 0
_y = -100
module.place(_x, _y, _w, _h)


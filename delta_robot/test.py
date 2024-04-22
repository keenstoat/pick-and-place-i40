#!/usr/bin/env python3

from delta_robot import DeltaRobot
from time import sleep

delta_robot_ip_addr = "192.168.3.11"

def main():

    dr = DeltaRobot(delta_robot_ip_addr)
    wait = True

    if dr.is_connected:

        dr.reset()
        dr.enable()
        dr.reference()

        dr.set_velocity(500)
        dr.set_position_endeffector(0, 0, 100)
        dr.move_endeffector(wait)
        
        # input("continue...")
        # dr.control_gripper(0,0)

        # input("continue...")
        # dr.control_gripper(50,45)

        # input("continue...")
        # dr.control_gripper(100,90)

        # input("continue...")
        # dr.control_gripper(50,135)

        # input("continue...")
        # dr.control_gripper(0,180)

        input("continue...")
        dr.set_velocity(50)
        # sleep(3)
        for z in range(0, 300, 50):
            print("Kinematics error: ", dr.get_kinematics_error())
            dr.set_position_endeffector(0, 0, z)
            dr.move_endeffector()
            print(dr.get_position_endeffector())
            # input("continue...")
            # sleep(3)

        # input("continue...")
        # dr.set_position_endeffector(100, 0, 150)
        # dr.move_endeffector(wait)

        # input("continue...")
        # dr.set_position_endeffector(0, 200, 150)
        # dr.move_endeffector(wait)

        # input("continue...")
        # dr.set_position_endeffector(-200, 200, 150)
        # dr.move_endeffector(wait)
    else:
        print("No Connection")

main()
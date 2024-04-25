#!/usr/bin/env python3

from delta_robot.delta_robot import DeltaRobot
from time import sleep

delta_robot_ip_addr = "192.168.3.11"

def main():

    dr = DeltaRobot(delta_robot_ip_addr)
    wait = True

    if dr.is_connected:


        dr.enable()
        
        if dr.get_kinematics_error():
            print("Kinematics errors found. Resetting..")
            dr.reset()
        
        dr.set_zero_torque(enable=False)
        if not dr.is_referenced() and not dr.reference():
            print("Coult NOT reference robot. Try again")
            return
        print("Robot is referenced!")

        # dr.set_all_axes_to_zero()
        dr.set_velocity(1000)

        xyz = [
            (0,0,0),
            (10, 10, 250),
            (-10, -10, 250),
            (20, 20, 250),
            (-20, -20, 250),
            (30, 30, 250),
            (-30, -30, 250),
            (100, 100, 250),
            (-100, -100, 250),
        ]

        for i, coord in enumerate(xyz):

            print()
            print(f"{i} - move to {coord} ====================================")
            dr.move_cartesian(*coord)
            print("k:", dr.get_kinematics_error())
            print("m:", dr.get_robot_errors())

        
        






        
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

        # input("continue...")
        # dr.set_velocity(50)
        # for z in range(0, 300, 50):
        #     print("Kinematics error: ", dr.get_kinematics_error())
        #     dr.set_position_endeffector(0, 0, z)
        #     dr.move_endeffector()
        #     print(dr.get_position_endeffector())


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
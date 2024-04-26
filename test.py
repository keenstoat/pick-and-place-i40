#!/usr/bin/env python3

from delta_robot.delta_robot import DeltaRobot
from time import sleep

# delta_robot_ip_addr = "192.168.3.11"
delta_robot_ip_addr = "localhost"
delta_robot_port = 5020

def main():

    dr = DeltaRobot(delta_robot_ip_addr, port=delta_robot_port)
    if dr.is_connected:

        print(dr.get_module_error_list())
        print(dr.get_kinematics_error())
        print("info or error: ", dr.get_info_or_message())

        dr.enable()
        if not dr.is_referenced():
            print("Robot NOT referenced. Resetting now.")
            dr.reset()
            if not dr.reference():
                print("Coult NOT reference robot. Try again")
                return
        print("Robot is referenced!")

        dr.set_override_velocity(100)
        dr.set_velocity(1000)

        xyz = [
            (150, 150, 200),
            (-150, 150, 200),
            (-150, -150, 200),
            (150, -150, 200),
        ]

        for _ in range(10):
            for i, coord in enumerate(xyz):
                print()
                print(f"{i} - move to {coord} ====================================")
                dr.move_cartesian(*coord)
                print("moved to > ", dr.get_target_position_cart())


        
        






        
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

        
    else:
        print("No Connection")

main()


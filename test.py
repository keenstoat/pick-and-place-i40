#!/usr/bin/env python3

from delta_robot.delta_robot import DeltaRobot
from time import sleep

# delta_robot_ip_addr = "192.168.3.11"
delta_robot_ip_addr = "localhost"
delta_robot_port = 5020

END_EFFECTOR_MAX_HEIGHT = 300

def main():

    table_distance = 600
    dr = DeltaRobot(table_distance, delta_robot_ip_addr, port=delta_robot_port)
    if dr.is_connected:
        print("Has General Error       : ", dr.has_module_error())
        print("Has Kinemat Error       : ", dr.has_kinematics_error())
        print()
        print("Module Error List   : ", dr.get_module_error_list())
        print("Kino Error List     : ", dr.get_kinematics_error_list())
        print("Kino error single   : ", dr.get_kinematics_error())
        print("Info or error short : ", dr.get_info_or_message())
        print()

        if not dr.is_referenced():
            print("Robot NOT referenced. Resetting now.")
            dr.reset()
            print("Enabling motors now..")
            dr.enable()
            print("Referencing now..")
            if not dr.reference():
                print("Coult NOT reference robot. Try again")
                return
        print("Robot is referenced!")

        dr.enable()
        dr.set_override_velocity(100)
        dr.set_velocity(500)

        xyz_grip = [
            # {"xyz": (0,0,300), "g": (0, 0)},
            # {"g": (100, 180)},
            # {"xyz": (0,0,0)},
            # {"g": (70, 180)},
            {"xyz": (0, 177, END_EFFECTOR_MAX_HEIGHT-180)},
        ]

        for _ in range(1):
            for i, coord in enumerate(xyz_grip):
                # input("..")
                xyz = coord.get("xyz")
                g = coord.get("g")
                print()
                print(f"{i} - move to   {xyz} ====================================")
                print(f"{i} - griper to {g} ====================================")
                if xyz:
                    dr.move_cartesian(*xyz)
                if g:
                    dr.control_gripper(*g)
                # print("moved to > ", dr.get_target_position_cart())

    else:
        print("No Connection")

main()


from flask import json, request
from gripper.gripper import Gripper
from delta_robot.delta_robot import DeltaRobot
import threading

ROBOT_BASE_TO_END_EFFECTOR_BASE_INITIAL_DISTANCE = 290 # mm
ROBOT_Z_RANGE = 300 # mm
GRIPPER_HEIGHT = 140 # mm

TABLE_DISTANCE_FROM_ROBOT_BASE = None


def status():
    delay = 15
    response = {
         "data": "status ok!"
    }
    def to_sleep(delay):
        from time import sleep
        print("SLEEP START!")
        sleep(delay)
        print("SLEEP STOP!")

    threading.Thread(target=to_sleep, args=[delay]).start()
    # to_sleep(delay)
    return json.dumps(response), 202

def init_module(delta_robot_ip_addr, delta_robot_port):
        
        gripper = Gripper()
        robot = DeltaRobot(delta_robot_ip_addr, port=delta_robot_port)
        assert robot.is_connected, "DeltaRobot is not connected"

        print("Has General Error       : ", robot.has_module_error())
        print("Has Kinemat Error       : ", robot.has_kinematics_error())
        print()
        print("Module Error List   : ", robot.get_module_error_list())
        print("Kino Error List     : ", robot.get_kinematics_error_list())
        print("Kino error single   : ", robot.get_kinematics_error())
        print("Info or error short : ", robot.get_info_or_message())
        print()

        if not robot.is_referenced():
            print("Robot NOT referenced. Resetting now.")
            robot.reset()
            print("Enabling motors now..")
            robot.enable()
            print("Referencing now..")
            if not robot.reference():
                print("Coult NOT reference robot. Try again")
                return
        print("Robot is referenced!")

        robot.enable()
        robot.set_override_velocity(100)
        robot.set_velocity(500)
        robot.move_cartesian(x=0, y=0, z=ROBOT_Z_RANGE)

        gripper.open_mm(0)
        gripper.rotate(90)

        response = {
            "data": ""
        }
        return json.dumps(response), 201

def set_table_distance():

    data = request.json["data"]

    global TABLE_DISTANCE_FROM_ROBOT_BASE
    TABLE_DISTANCE_FROM_ROBOT_BASE = float(data)

    response = {
         "data": ""
    }
    return json.dumps(response), 201

def get_robot_lowest_position():
    z = ROBOT_Z_RANGE - (TABLE_DISTANCE_FROM_ROBOT_BASE - ROBOT_BASE_TO_END_EFFECTOR_BASE_INITIAL_DISTANCE) + GRIPPER_HEIGHT

    response = {
         "data": z
    }
    return json.dumps(response), 200


x = 0
y = 0
z = 0
def set_robot_position():
    global x, y, z

    if request.method == "GET":
        response = {
            "data": {"x": x, "y": y, "z": z}
        }
        return json.dumps(response), 200
    print("DATA: ", request.data.decode())
    data = request.json['data']
    if "x" in data:
        x = float(data["x"])
    
    if "y" in data:
        y = float(data["y"])
    
    if "z" in data:
        z = float(data["z"])

    return '', 201

    


    


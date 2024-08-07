from flask import json, request
from gripper.gripper import Gripper
from delta_robot.delta_robot import DeltaRobot
import threading
from time import sleep

ROBOT_BASE_TO_END_EFFECTOR_BASE_INITIAL_DISTANCE = 290 # mm
ROBOT_Z_RANGE = 300 # mm
GRIPPER_HEIGHT = 140 # mm

TABLE_DISTANCE_FROM_ROBOT_BASE = None


DELTA_ROBOT_IP_ADDRESS = "192.168.3.11"
DELTA_ROBOT_PORT = 502


def status():
    response = {
         "data": "status ok!"
    }
    return json.dumps(response), 200

def is_module_initialized():

    robot = DeltaRobot(DELTA_ROBOT_IP_ADDRESS, port=DELTA_ROBOT_PORT)
    response = {
        "data": robot.is_enabled() and robot.is_referenced()
    }
    return json.dumps(response), 200

def init_module():
        
        def init():
            gripper = Gripper()
            robot = DeltaRobot(DELTA_ROBOT_IP_ADDRESS, port=DELTA_ROBOT_PORT)
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
            robot.set_speed(200)
            robot.move_cartesian(x=0, y=0, z=ROBOT_Z_RANGE)
            robot.set_speed(100)

            gripper.open_mm(0)
            gripper.rotate(90)

        threading.Thread(target=init, args=[]).start()
        response = {
            "data": ""
        }
        return json.dumps(response), 202

def set_table_distance():

    data = request.json["data"]

    global TABLE_DISTANCE_FROM_ROBOT_BASE
    TABLE_DISTANCE_FROM_ROBOT_BASE = float(data)

    response = {
         "data": ""
    }
    return json.dumps(response), 201

def get_robot_position_xyz():

    coord = request.url.split("/")[-1]

    robot = DeltaRobot(DELTA_ROBOT_IP_ADDRESS, port=DELTA_ROBOT_PORT)
    x, y, z = robot.get_target_position_cart()

    data = {"x": x, "y": y, "z": z}

    if coord in ("x", "y", "z"):
        data = data[coord]
        
    response = {
        "data": data
    }
    return json.dumps(response), 200

def get_set_robot_speed():

    robot = DeltaRobot(DELTA_ROBOT_IP_ADDRESS, port=DELTA_ROBOT_PORT)

    if request.method == "GET":
        response = {
            "data": robot.get_speed()
        }
        return json.dumps(response), 200

    speed = request.json["data"]
    robot.set_speed(speed)
    return '', 201
    
def move_robot():
 
    xyzs:dict = request.json["data"]

    for coord, value in xyzs.items():
        xyzs[coord] = float(value) if value.strip() else None
    
    if xyzs["speed"]:
        xyzs["speed"] = int(xyzs["speed"])

    robot = DeltaRobot(DELTA_ROBOT_IP_ADDRESS, port=DELTA_ROBOT_PORT)
    threading.Thread(target=robot.move_cartesian, args=[xyzs["x"], xyzs["y"], xyzs["z"], xyzs["speed"]]).start()
    response = {
        "data": ""
    }
    return json.dumps(response), 202

def is_module_busy():

    robot = DeltaRobot(DELTA_ROBOT_IP_ADDRESS, port=DELTA_ROBOT_PORT)
    response = {
        "data": robot.is_moving()
    }
    return json.dumps(response), 200

# aux functions ========================================================================================================

def get_robot_lowest_position():
    z = ROBOT_Z_RANGE - (TABLE_DISTANCE_FROM_ROBOT_BASE - ROBOT_BASE_TO_END_EFFECTOR_BASE_INITIAL_DISTANCE) + GRIPPER_HEIGHT

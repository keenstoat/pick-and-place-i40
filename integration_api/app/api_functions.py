from flask import json, request
from gripper.gripper import Gripper
from delta_robot.delta_robot import DeltaRobot
import threading
from time import sleep

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


_is_module_busy = False
target_position = {
    "x": 0, "y": 0, "z": 0
}

real_position = {
    "x": 0, "y": 0, "z": 0
}

# TODO this is a mock
def set_target_position_cart(x:float=None, y:float=None, z:float=None):
    if x is not None:
        target_position["x"] = x

    if y is not None:
        target_position["y"] = y

    if z is not None:
        target_position["z"] = z

# TODO this is a mock
def get_target_position_cart():
    return real_position["x"], real_position["y"], real_position["z"]

# TODO this is a mock
def move_cartesian(x:float=None, y:float=None, z:float=None):
    global _is_module_busy
    _is_module_busy = True
    
    set_target_position_cart(x, y, z)
    delta_x = (target_position["x"] - real_position["x"])/10
    delta_y = (target_position["y"] - real_position["y"])/10
    delta_z = (target_position["z"] - real_position["z"])/10
    for _ in range(10):
        real_position["x"] += delta_x
        real_position["y"] += delta_y
        real_position["z"] += delta_z
        sleep(1)
    
    _is_module_busy = False

# POST must update the target position in holding registers
# GET must return the target position in input registers
def get_robot_position_xyz():
    coord = request.url.split("/")[-1]

    if request.method == "GET":
        x, y, z = get_target_position_cart()
        response = {
            "data": {"x": x, "y": y, "z": z}[coord]
        }
        return json.dumps(response), 200

    # # POST
    # data = request.json['data']
    # data = float(data)
    # match coord:
    #     case "x": set_target_position_cart(x=data)
    #     case "y": set_target_position_cart(y=data)
    #     case "z": set_target_position_cart(z=data)

    # return '', 201


def move_robot():
 
    xyz:dict = request.json["data"]

    for coord, value in xyz.items():
        xyz[coord] = float(value) if value.strip() else None

    threading.Thread(target=move_cartesian, args=[xyz["x"], xyz["y"], xyz["z"]]).start()
    response = {
        "data": ""
    }
    return json.dumps(response), 202


def is_module_busy():

    response = {
        "data": _is_module_busy
    }
    return json.dumps(response), 200
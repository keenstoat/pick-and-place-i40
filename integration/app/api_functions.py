from flask import json, request
from gripper.gripper import Gripper
from delta_robot.delta_robot import DeltaRobot
import threading
from os import environ

ROBOT_BASE_TO_END_EFFECTOR_BASE_INITIAL_DISTANCE = 290 # mm
ROBOT_Z_RANGE = 300 # mm
GRIPPER_HEIGHT = 140 # mm

_ROBOT_IP_ADDRESS = "192.168.3.11"
_ROBOT_PORT = 502

_table_distance_from_robot_base = None

_pick_and_place_active = False

# memoized gripper object
_gripper = None

def info():
    response = {
        "data": {
            "author": "carlos.josue.rene.avila.carrillo@stud.hs-emden-leer.de",
            "date": "september 2024",
            "description": "Integration application to monitor and control a few aspects of the Delta Robot and the Gripper of the pick and place module in the Technikum's Digital Factory."
        }
    }
    return json.dumps(response), 200

def is_module_initialized():

    robot = _get_robot()
    response = {
        "data": robot.is_enabled() and robot.is_referenced()
    }
    return json.dumps(response), 200

def initialize_module():
        
        threading.Thread(target=_init_module, args=[]).start()
        response = {
            "data": ""
        }
        return json.dumps(response), 202

def get_set_table_distance():

    global _table_distance_from_robot_base

    if request.method == "GET":
        response = {
            "data": _table_distance_from_robot_base or -1
        }
        return json.dumps(response), 200

    distance = request.json["data"]
    _table_distance_from_robot_base = int(distance)
    return '', 201

def get_gripper_position():

    coord = request.url.split("/")[-1]

    gripper = _get_gripper()
    data = gripper.get_status()

    if coord in ("opening", "rotation"):
        data = data[coord]
        
    response = {
        "data": data
    }
    return json.dumps(response), 200

def get_robot_position_xyz():

    coord = request.url.split("/")[-1]

    robot = _get_robot()
    x, y, z = robot.get_target_position_cart()

    data = {"x": x, "y": y, "z": z}

    if coord in ("x", "y", "z"):
        data = data[coord]
        
    response = {
        "data": data
    }
    return json.dumps(response), 200

def get_set_robot_speed():

    robot = _get_robot()

    if request.method == "GET":
        response = {
            "data": robot.get_speed()
        }
        return json.dumps(response), 200

    speed = request.json["data"]
    robot.set_speed(speed)
    return '', 201
    
def is_module_busy():

    robot = _get_robot()
    response = {
        "data": robot.is_moving() or _pick_and_place_active
    }
    return json.dumps(response), 200

def move_robot():
 
    xyzs:dict = request.json["data"]

    for coord, value in xyzs.items():
        xyzs[coord] = float(value) if value.strip() else None
    
    if xyzs["speed"]:
        xyzs["speed"] = int(xyzs["speed"])

    robot = _get_robot()
    threading.Thread(target=robot.move_cartesian, args=[xyzs["x"], xyzs["y"], xyzs["z"], xyzs["speed"]]).start()
    response = {
        "data": ""
    }
    return json.dumps(response), 202

def move_gripper():
    coords:dict = request.json["data"]

    opening = coords["opening"].strip()
    if opening:
        _get_gripper().open(int(opening))

    rotation = coords["rotation"].strip()
    if rotation:
        _get_gripper().rotate(int(rotation))
    
    response = {
        "data": ""
    }
    return json.dumps(response), 201

def pick_and_place():

    data = request.json["data"]
    x_ini = data["xInitial"]
    y_ini = data["yInitial"]
    x_end = data["xFinal"]
    y_end = data["yFinal"]
    object_width = data["objectWidth"]
    object_height = data["objectHeight"]

    def do():
        global _pick_and_place_active
        _pick_and_place_active = True
        robot = _get_robot()
        gripper = _get_gripper()
        robot_lowest_position = _get_robot_lowest_position()
        z_ini = robot_lowest_position + object_height + 10 # mm

        # Pick Object =======================================================
        # step("position above object")
        robot.move_cartesian(x=x_ini, y=y_ini, z=z_ini)
        
        # step("open gripper...")
        gripper.open(object_width + 10)

        # step("position to grab object")
        robot.move_cartesian(z=robot_lowest_position)
        
        # step("close gripper...")
        gripper.open(object_width-5)

        # step("pick up object")
        robot.move_cartesian(x=0, y=0, z=ROBOT_Z_RANGE)

        # Place Object =======================================================
        # step("position to place object")
        robot.move_cartesian(x=x_end, y=y_end, z=robot_lowest_position)
        
        # step("open gripper...")
        gripper.open(object_width + 10)

        # step("position above object")
        robot.move_cartesian(z=z_ini)

        # step("return to base position")
        robot.move_cartesian(x=0, y=0, z=ROBOT_Z_RANGE)
        
        # step("close gripper...")
        gripper.open(0)
        _pick_and_place_active = False

    threading.Thread(target=do, args=[]).start()
    response = {
        "data": ""
    }
    return json.dumps(response), 202

# aux functions ========================================================================================================

def _init_module():
    gripper = _get_gripper()
    robot = _get_robot()
    
    print("Has General Error       : ", robot.has_module_error())
    print("Has Kinemat Error       : ", robot.has_kinematics_error())
    print()
    print("Module Error List   : ", robot.get_module_error_list())
    print("Kino Error List     : ", robot.get_kinematics_error_list())
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

    gripper.open(0)
    gripper.rotate(90)

def _get_robot_lowest_position():
    z = ROBOT_Z_RANGE - (_table_distance_from_robot_base - ROBOT_BASE_TO_END_EFFECTOR_BASE_INITIAL_DISTANCE) + GRIPPER_HEIGHT
    return z

def _get_robot():
    
    robot_ip_address = environ.get("ROBOT_IP_ADDRESS", _ROBOT_IP_ADDRESS)
    robot_port = int(environ.get("ROBOT_PORT", _ROBOT_PORT))

    robot = DeltaRobot(robot_ip_address, port=robot_port)
    assert robot.is_connected, f"DeltaRobot could not connect to {robot_ip_address} on port {robot_port}"
    return robot
    
def _get_gripper():
    
    global _gripper

    if not _gripper:
        _gripper = Gripper()
    
    return _gripper
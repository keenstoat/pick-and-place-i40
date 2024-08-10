from flask import json, request
import threading
from os import environ
from time import sleep

ROBOT_BASE_TO_END_EFFECTOR_BASE_INITIAL_DISTANCE = 290 # mm
ROBOT_Z_RANGE = 300 # mm
GRIPPER_HEIGHT = 140 # mm

_table_distance_from_robot_base = None

_opening = 0
_rotation = 0
class Gripper:
    
    def get_status(self):
        return {"opening": _opening, "rotation": _rotation}
    def open(self, val):
        global _opening
        _opening = val
    def rotate(self, val):
        global _rotation
        _rotation = val

class DeltaRobot:

    _is_enabled = False
    _is_referenced = False
    x,y,z = 0,0,0
    speed = 100
    _is_moving = False
    def is_enabled(self):
        return self._is_enabled
    def is_referenced(self):
        return self._is_referenced
    def get_target_position_cart(self):
        return self.x, self.y, self.z
    def get_speed(self):
        return self.speed
    def set_speed(self, speed):
        self.speed = speed
    def is_moving(self):
        return self._is_moving
    def move_cartesian(self, x=None, y=None, z=None, speed=None):
        
        dx = (x-self.x)/10 if x is not None else 0
        dy = (y-self.y)/10 if y is not None else 0
        dz = (z-self.z)/10 if z is not None else 0

        if speed:
            self.speed = speed
        self._is_moving = True
        for _ in range(10):
            self.x+=dx
            self.y+=dy
            self.z+=dz
            print(f"{self.x}, {self.y}, {self.z}")
            sleep(0.3)
        self._is_moving = False

def status():
    response = {
         "data": "status ok!"
    }
    return json.dumps(response), 200

def is_module_initialized():

    robot = get_robot()
    response = {
        "data": robot.is_enabled() and robot.is_referenced()
    }
    return json.dumps(response), 200

def initialize_module():
        
        threading.Thread(target=init_module, args=[]).start()
        response = {
            "data": ""
        }
        return json.dumps(response), 202

def set_table_distance():

    global _table_distance_from_robot_base

    data = request.json["data"]
    _table_distance_from_robot_base = float(data)

    response = {
         "data": ""
    }
    return json.dumps(response), 201

def get_gripper_position():

    coord = request.url.split("/")[-1]

    gripper = Gripper()
    data = gripper.get_status()

    if coord in ("opening", "rotation"):
        data = data[coord]
        
    response = {
        "data": data
    }
    return json.dumps(response), 200

def get_robot_position_xyz():

    coord = request.url.split("/")[-1]

    robot = get_robot()
    x, y, z = robot.get_target_position_cart()

    data = {"x": x, "y": y, "z": z}

    if coord in ("x", "y", "z"):
        data = data[coord]
        
    response = {
        "data": data
    }
    return json.dumps(response), 200

def get_set_robot_speed():

    robot = get_robot()

    if request.method == "GET":
        response = {
            "data": robot.get_speed()
        }
        return json.dumps(response), 200

    speed = request.json["data"]
    robot.set_speed(speed)
    return '', 201
    
def is_module_busy():

    robot = get_robot()
    response = {
        "data": robot.is_moving()
    }
    return json.dumps(response), 200

def move_robot():
 
    xyzs:dict = request.json["data"]

    for coord, value in xyzs.items():
        xyzs[coord] = float(value) if value.strip() else None
    
    if xyzs["speed"]:
        xyzs["speed"] = int(xyzs["speed"])

    robot = get_robot()
    threading.Thread(target=robot.move_cartesian, args=[xyzs["x"], xyzs["y"], xyzs["z"], xyzs["speed"]]).start()
    response = {
        "data": ""
    }
    return json.dumps(response), 202

def move_gripper():
    coords:dict = request.json["data"]

    opening = coords["opening"].strip()
    if opening:
        Gripper().open(int(opening))

    rotation = coords["rotation"].strip()
    if rotation:
        Gripper().rotate(int(rotation))
    
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
        robot = get_robot()
        gripper = Gripper()
        robot_lowest_position = get_robot_lowest_position()
        z_ini = robot_lowest_position + object_height + 10 # mm

        # Pick Object =======================================================
        print("position above object")
        robot.move_cartesian(x=x_ini, y=y_ini, z=z_ini)
        
        print("open gripper...")
        gripper.open(object_width + 10)

        print("position to grab object")
        robot.move_cartesian(z=robot_lowest_position)
        
        print("close gripper...")
        gripper.open(object_width-5)

        print("pick up object")
        robot.move_cartesian(x=0, y=0, z=ROBOT_Z_RANGE)

        # Place Object =======================================================
        print("position to place object")
        robot.move_cartesian(x=x_end, y=y_end, z=robot_lowest_position)
        
        print("open gripper...")
        gripper.open(object_width + 10)

        print("position above object")
        robot.move_cartesian(z=z_ini)

        print("return to base position")
        robot.move_cartesian(x=0, y=0, z=ROBOT_Z_RANGE)
        
        print("close gripper...")
        gripper.open(0)

    threading.Thread(target=do, args=[]).start()
    response = {
        "data": ""
    }
    return json.dumps(response), 202

# aux functions ========================================================================================================
def init_module():
    global _rotation, _opening
    robot = get_robot()
    
    robot._is_enabled = True
    robot._is_referenced = True
    _opening = 0
    _rotation = 0

def get_robot_lowest_position():
    z = ROBOT_Z_RANGE - (_table_distance_from_robot_base - ROBOT_BASE_TO_END_EFFECTOR_BASE_INITIAL_DISTANCE) + GRIPPER_HEIGHT
    return z


_robot = None
def get_robot():
    global _robot

    if not _robot:
        _robot = DeltaRobot()
    
    return _robot
    
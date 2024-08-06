from flask import json, request
from delta_robot.delta_robot import DeltaRobot
from os import environ

delta_robot_ip_addr = environ.get("DELTA_MODBUSTCP_IP_ADDRESS")
delta_robot_port = environ.get("DELTA_MODBUSTCP_PORT")

delta_robot = DeltaRobot(delta_robot_ip_addr, port=delta_robot_port)

def get_position_cartesian():

    x, y, z = delta_robot.get_target_position_cart()
    response = {
        "data": {
            "x": x,
            "y": y,
            "z": z
        }
    }
    return json.dumps(response), 200

def move_to():
     
    data = request.json["data"]
    x = data.get("x", None)
    y = data.get("y", None)
    z = data.get("z", None)
    speed = data.get("speed", None)

    delta_robot.move_cartesian(x=x, y=y, z=z, velocity=speed)
    return "", 201

def pickup():

    data = request.json
    data = list(data.values())
    print("Calling pickup with: ", data)
    response = {
        "data": f"called as pickup({data})"
    }
    return json.dumps(response)

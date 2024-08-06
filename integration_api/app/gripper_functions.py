
from flask import json, request
#import paramiko
from gripper.gripper import Gripper

def rotate():

    if request.method != "POST":
        return 400
    
    value = request.json["data"]
    value = int(value)
    Gripper().rotate(value, relative=False)

    response = {
        "data": f"rotation complete to {value} degrees"
    }
    return json.dumps(response), 201

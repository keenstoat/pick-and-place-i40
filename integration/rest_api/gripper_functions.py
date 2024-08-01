
from flask import json, request
#import paramiko
from gripper.gripper import Gripper

def rotate():

    if request.method != "POST":
        return 400
    

    value = request.json["data"]
    value = int(value)
    # ssh = paramiko.SSHClient()
    # ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    # ssh.connect("192.168.158.89", username="charles", password="asdf123")
    # ssh.exec_command(f"sudo ./gripper.py rotate {value}")

    Gripper().rotate(value, relative=False)

    response = {
        "data": f"rotation complete to {value} degrees"
    }
    return json.dumps(response), 201

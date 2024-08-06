#!/usr/bin/env python3

from flask import Flask
# from gripper_functions import *
# from robot_functions import *

from api_functions import *

api = Flask(__name__)



# @api.route("/status", methods=['GET'])
# def status():
#     return '{"data": "status ok!"}', 200
api.add_url_rule("/status", view_func=status, methods=['GET', 'POST'])

# api.add_url_rule("/FunctionsSubModel/rotate", view_func=rotate, methods=['POST'])

api.add_url_rule("/OperationalData/robotPosition", view_func=set_robot_position, methods=['GET', 'POST'])
# api.add_url_rule("/FunctionsSubModel/moveTo", view_func=move_to, methods=['POST'])

if __name__ == '__main__':
    api.run(host="0.0.0.0", port="8080")

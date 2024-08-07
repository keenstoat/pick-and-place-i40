#!/usr/bin/env python3

from flask import Flask
# from gripper_functions import *
# from robot_functions import *

from api_functions import *

api = Flask(__name__)



# @api.route("/status", methods=['GET'])
# def status():
#     return '{"data": "status ok!"}', 200

api.add_url_rule("/status", view_func=status, methods=['GET'])

api.add_url_rule("/OperationalData/isModuleInitialized", view_func=is_module_initialized, methods=['GET'])
api.add_url_rule("/OperationalData/initModule", view_func=init_module, methods=['POST'])
api.add_url_rule("/OperationalData/setTableDistance", view_func=set_table_distance, methods=['POST'])

api.add_url_rule("/OperationalData/robotPosition",   view_func=get_robot_position_xyz, methods=['GET'])
api.add_url_rule("/OperationalData/robotPosition/x", view_func=get_robot_position_xyz, methods=['GET'])
api.add_url_rule("/OperationalData/robotPosition/y", view_func=get_robot_position_xyz, methods=['GET'])
api.add_url_rule("/OperationalData/robotPosition/z", view_func=get_robot_position_xyz, methods=['GET'])

api.add_url_rule("/OperationalData/isModuleBusy", view_func=is_module_busy, methods=['GET'])
api.add_url_rule("/OperationalData/moveRobot", view_func=move_robot, methods=['POST'])

if __name__ == '__main__':
    api.run(host="0.0.0.0", port="8080")

#!/usr/bin/env python3

from flask import Flask
from api_functions import * # TODO change back to real functions

api = Flask(__name__)

api.add_url_rule("/info", view_func=info, methods=['GET'])

api.add_url_rule("/OperationalData/isModuleInitialized", view_func=is_module_initialized, methods=['GET'])
api.add_url_rule("/OperationalData/isModuleBusy", view_func=is_module_busy, methods=['GET'])
api.add_url_rule("/OperationalData/robotSpeed", view_func=get_set_robot_speed, methods=['GET', 'POST'])
api.add_url_rule("/OperationalData/tableDistance", view_func=get_set_table_distance, methods=['GET', 'POST'])

api.add_url_rule("/OperationalData/robotPosition",   view_func=get_robot_position_xyz, methods=['GET'])
api.add_url_rule("/OperationalData/robotPosition/x", view_func=get_robot_position_xyz, methods=['GET'])
api.add_url_rule("/OperationalData/robotPosition/y", view_func=get_robot_position_xyz, methods=['GET'])
api.add_url_rule("/OperationalData/robotPosition/z", view_func=get_robot_position_xyz, methods=['GET'])

api.add_url_rule("/OperationalData/gripperPosition",          view_func=get_gripper_position, methods=['GET'])
api.add_url_rule("/OperationalData/gripperPosition/opening",  view_func=get_gripper_position, methods=['GET'])
api.add_url_rule("/OperationalData/gripperPosition/rotation", view_func=get_gripper_position, methods=['GET'])

api.add_url_rule("/OperationalData/initializeModule", view_func=initialize_module, methods=['POST'])
api.add_url_rule("/OperationalData/moveRobot", view_func=move_robot, methods=['POST'])
api.add_url_rule("/OperationalData/moveGripper", view_func=move_gripper, methods=['POST'])
api.add_url_rule("/OperationalData/pickAndPlace", view_func=pick_and_place, methods=['POST'])

if __name__ == '__main__':
    api.run(host="0.0.0.0", port="8080")

#!/usr/bin/env python3

from flask import Flask
from gripper_functions import *

api = Flask(__name__)

api.add_url_rule("/FunctionsSubModel/rotate", view_func=rotate, methods=['POST'])


if __name__ == '__main__':
    api.run(host='0.0.0.0', port=8080)

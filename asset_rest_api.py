#!/usr/bin/env python3

from flask import Flask, json, request
from random import randint


api = Flask(__name__)

asset_values = {
    "processedItemCount": 0
}

@api.route('/FunctionsSubModel/processedItemCount', methods=['GET', 'POST'])
def processed_item_count():

    if request.method == "GET":
        data = asset_values["processedItemCount"]
        print("READ processedItemCount: ", data)
        response = {
            "data": data
        }
        return json.dumps(response), 200
    
    data = request.json["data"]
    print("WRITE processedItemCount: ", data)
    asset_values["processedItemCount"] = int(data)
    return "", 204


@api.route('/FunctionsSubModel/pickup', methods=['POST'])
def pickup():

    data = request.json
    data = list(data.values())
    print("Calling pickup with: ", data)
    response = {
        "data": f"called as pickup({data})"
    }
    return json.dumps(response)


if __name__ == '__main__':
    api.run(port=8080)

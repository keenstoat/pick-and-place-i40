from flask import json, request

asset_values = {
    "processedItemCount": 0
}

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


def pickup():

    data = request.json
    data = list(data.values())
    print("Calling pickup with: ", data)
    response = {
        "data": f"called as pickup({data})"
    }
    return json.dumps(response)

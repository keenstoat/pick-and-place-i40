#!/usr/bin/env python3

import yaml
import json

# Function to convert YAML to JSON
def yaml_to_json(yaml_filepath, json_filepath):
    try:
        # Read the YAML file
        with open(yaml_filepath, 'r') as yaml_file:
            yaml_content = yaml.safe_load(yaml_file)

        # Write the JSON file
        with open(json_filepath, 'w') as json_file:
            json.dump(yaml_content, json_file, indent=4)

    except Exception as e:
        print(f"Error: {e}")

# Example usage
yaml_filepath = 'config-opcua-http.yaml'
json_filepath = 'config-opcua-http.json'
yaml_to_json(yaml_filepath, json_filepath)

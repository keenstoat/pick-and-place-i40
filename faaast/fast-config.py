#!/usr/bin/env python3

import yaml
import json
import sys

def yaml_to_json():
    with open("aasx/config.yaml") as yaml_file:
        configuration = yaml.safe_load(yaml_file)

    with open('aasx/config.json', 'w') as json_file:
        json.dump(configuration, json_file, indent=2)

def json_to_yaml():
    with open('aasx/config.json') as json_file:
        config = json.load(json)

    with open("aasx/config.yaml", 'w') as yaml_file:
        yaml.dump(config, yaml_file)

    

args = sys.argv
args.pop(0)

if not args:
    print("must define an action: toyaml or tojson")
    sys.exit(1)
    
action = args.pop(0)
match action:
    case "toyaml":
        json_to_yaml()
    case "tojson":
        yaml_to_json()
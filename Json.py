import json
import os

conf = dict()

def update_conf(conf_file):
    global conf
    conf = dict()
    if os.path.getsize(conf_file) > 0:
        with open(conf_file, "r") as read_file:
            conf = json.load(read_file)

def save_json(idict, json_file, mode):
    with open(json_file, mode) as write_file:
        json.dump(idict, write_file, indent=4)

def load_json(json_file):
    j = dict()
    if os.path.getsize(json_file) > 0:
        with open(json_file, "r") as read_file:
            j = json.load(read_file)
    return j

def update_json(newdata, json_file):
    j = load_json(json_file)
    j.update(newdata)
    save_json(j,json_file,'w')
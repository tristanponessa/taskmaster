import json
import os

conf = dict()

def load_json(conf_file):
    global conf
    conf = dict()
    if os.path.getsize(conf_file) > 0:
        with open(conf_file, "r") as read_file:
            conf = json.load(read_file)
    
    


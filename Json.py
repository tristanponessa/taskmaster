import json
import os

#conf_file = './config/taskmaster_conf.json'
conf = dict()

"""
def ft_json(option, j=None):
    try:
        if option == 'save':
            
        if option == 'load':
    
    
    any json error
"""

"""
def save_json(j):
    with open(conf_file, "w") as write_file:
        json.dump(j, write_file, indent=4)
"""

def load_json(conf_file):
    global conf
    conf = dict()
    if os.path.getsize(conf_file) > 0:
        with open(conf_file, "r") as read_file:
            conf = json.load(read_file)
    
    


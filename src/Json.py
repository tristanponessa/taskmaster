import json
import os
import Global
import Process as psFILE

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

def reload_conf():
    global conf
    new_conf = load_json(f'{Global.conf_file}')

    not_touch = []
    for name,prg in conf.items():
        for new_name,new_prg in new_conf.items():
            if name == new_name and \
                prg == new_prg:
                    not_touch.append(name)
                        
    pss_names = psFILE.pss.keys()
    for pss_n in pss_names:
        if pss_n not in not_touch:
            psFILE.pss[pss_n].ps['popen'].kill()
            del psFILE.pss[pss_n]

    #from ts 
    for ps,props in new_conf.items():
        if ps not in not_touch:
            psFILE.pss[ps] = []
            nps = psFILE.Process(ps, props)
            nbps = int(nps.ps['nbps'])
            for i in range(nbps):
                nps = psFILE.Process(ps, props)
                if nps.ps['autostart'] == "yes": 
                    Global.printx(f"{ps} : autostart")
                    nps.start_ps()
                psFILE.pss[ps].append(nps)





    
    


    
    
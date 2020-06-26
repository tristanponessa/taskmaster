"""
    conf is a json
"""

import json
import os
import Global
import Process as psFILE

conf = dict()
dft_conf =  {
                'cmd':          'sh sec_counter.bash',
                'nbps':         '1',
                'timetillsuc':  '0',
                'autostart':    'no',
                'autorestart':  'no',
                'stoptime':     '0',
                'dir':          './',
                'env':          "",
                'stdout':       f'./dft_stdout.stdout',
                'stderr':       f'./dft_stderr.stderr',
                'nbretries':    '0',#if crashes, restarts
                'exitsignal':   'TERM',#SIGTERM
                'exitcode':     '0',
                'umask':        '022'
            }


def is_confFile(conf):
    err = []
    
    msg = f'error : config file <{conf}>'
    if not os.path.exists(conf):
        err.append(f"{msg} don't exist")
    if not conf.endswith('.json'):
        err.append(f"{msg} don't end with json")
    if os.path.getsize(conf) > 0:
        err.append(f"{msg} is empty")
    return err

def get_psProp(psName, propName):
    global conf, dft_conf
    if psName in conf.keys():
        return conf[psName][propName] 
    return dft_conf[propName]

def load_Aconf(json_file):
    conf = dict()
    if is_confFile(json_file) != []:
        with open(json_file, "r") as read_file:
            conf = json.load(read_file)
    return conf

"""
def dict_sameItems(oldD, newD):
    same = set()
    for ok,ov in oldD.items():
        for nk,nv in newD.items():
            if nk == ok and nv == ov:
                same.update([ok])
    return same
"""

def confReload(json_file):
    """
        if conf reloaded , dont kill pss that dont change props
    """
    global conf
    new_conf = load_Aconf(json_file) #json get $ user input file
    #old_conf = conf 
    #protected = dict_sameItems(old_conf, new_conf)
    #LOG
    conf = new_conf.copy() 
    #return protected

#never need to save
"""
def save_conf(idict, json_file, mode):
    with open(json_file, mode) as write_file:
        json.dump(idict, write_file, indent=4)
"""

"""
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
"""




    
    


    
    
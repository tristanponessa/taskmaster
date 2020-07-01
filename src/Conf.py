"""
    conf is a json
"""

import json
import os

import Global
import Process as pgFILE

conf = dict()
dft_conf =  {
                'cmd':          'ls -l',
                'nbps':         '1',
                'timetillsuc':  '0',
                'autostart':    'no',
                'autorestart':  'no',
                'stoptime':     '0',
                'workdir':      './',
                'env':          {"TEST":"TEST"},
                'stdout':       f'./logs/dft_stdout.stdout',
                'stderr':       f'./logs/dft_stderr.stderr',
                'restart':      'no',#if crashes, restarts
                'nbrestart':   '5',
                'exitcode':   'SIGINT',#SIGINT
                'returncode':   '1',
                'umask':        '022'
            }

#LOG
def is_confFile(conf):
    err = []
    
    msg = f'error : config file <{conf}>'
    if not os.path.exists(conf):
        err.append(f"{msg} don't exist")
    elif os.path.getsize(conf) <= 0:
        err.append(f"{msg} is empty")
    if not conf.endswith('.json'):
        err.append(f"{msg} don't end with json")
    
    return err

def get_pgProp(pgName, propName):
    global conf, dft_conf
    if pgName in conf.keys() and propName in conf[pgName]:
        return conf[pgName][propName] 
    return dft_conf[propName]

def load_Aconf(json_file):
    conf = dict()
    if is_confFile(json_file) == []:
        with open(json_file, "r") as read_file:
            conf = json.load(read_file)
    return conf

def confReload(json_file):
    """
        if conf reloaded , dont kill pgs that dont change propg
    """
    global conf
    new_conf = load_Aconf(json_file) #json get $ user input file
    conf = new_conf.copy()
    #old_conf = conf 
    #protected = dict_sameItems(old_conf, new_conf)
    #LOG
     
    #return protected

"""
def dict_sameItems(oldD, newD):
    same = set()
    for ok,ov in oldD.items():
        for nk,nv in newD.items():
            if nk == ok and nv == ov:
                same.update([ok])
    return same
"""


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
                        
    pgs_names = pgFILE.pgs.keys()
    for pgs_n in pgs_names:
        if pgs_n not in not_touch:
            pgFILE.pgs[pgs_n].pg['popen'].kill()
            del pgFILE.pgs[pgs_n]

    #from ts 
    for pg,propg in new_conf.items():
        if pg not in not_touch:
            pgFILE.pgs[pg] = []
            npg = pgFILE.Process(pg, propg)
            nbpg = int(npg.pg['nbpg'])
            for i in range(nbpg):
                npg = pgFILE.Process(pg, propg)
                if npg.pg['autostart'] == "yes": 
                    Global.printx(f"{pg} : autostart")
                    npg.start_pg()
                pgFILE.pgs[pg].append(npg)
"""




    
    


    
    
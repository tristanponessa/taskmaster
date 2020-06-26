        """
        if (key in confk) and (key not in pssk):
            init_ps(key)
        elif (key not in confk):
            destroy_ps(key)
        elif (key in confk) and (pss[key][0].props != confFILE.conf[key]):
            destroy_ps(key)
            init_ps()
        """
        #if key in conf AND val same name props:
        #    NOTHING
    """
    if protected is not None:
        for psName in pss.keys():
            if psName not in protected:
                destroy_ps()    #else:
                ###add rest
    else:
        pss.clear()
    #only stop those who are active
    for psName in confFILE.conf.keys():
        if psName not in protected:
            init_ps(psName)
    """






    """
    def ft_thread(ft):
        p = threading.Thread(target=ft)
        p.deamon = True
        p.start()
        return p

    def kill_leftover():
        
        #    keep all dead ps as zombies 
        #    so the os dont give the pid to another
        #    or youll be killing outside ps
        
        d = jsonFILE.load_json(pss_json)
        for pid,info in d.items():
            pid = int(pid)
            state = 'already dead'
            if psutil.pid_exists(pid):
                pp = psutil.Process(pid)
                state = pp.status()
                os.kill(pid, signal.SIGKILL)    
            printx(f"PID {pid} NAME {info['name']} CMD {info['cmd']} state > {state}")
"""
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
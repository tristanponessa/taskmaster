import Global

def autostart_msg(psName):
    Global.printx(f"AUTOSTART <{psName}>")

def returncode_msg(psName, conf_returncode, psReturncode):
    msg = f"ps {Global.now_time()} {psName} ended  returncode:{psReturncode} expecting {conf_returncode}  "
    msg += 'fail'
    if conf_returncode == str(psReturncode):
        msg += 'success'
    Global.print_file(msg, Global.tk_res, 'a')
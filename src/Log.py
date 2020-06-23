def autostart_msg(psName):
    Global.printx(f"AUTOSTART <{psName}>")

def returncode_msg(cmd, returncode, psExitcode):
    msg = f"ps {cmd} ended  returncode:{returncode} expecting {self.ps['exitcode']}  "
    msg += 'fail'
    if str(returncode) == self.ps['exitcode']:
        msg += 'success'
    Global.print_file(msg, Global.tk_res, 'a')
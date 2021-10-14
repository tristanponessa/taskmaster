

class MyDict(dict):
    
    def __init__(self,*arg,**kw):
        super(MyDict, self).__init__(*arg, **kw)
        self.x = []
        
    def __setitem__(self, item, value):
        print (f"You are changing the value of {item} to {value}!!")
        super(MyDict, self).__setitem__(item, value)
        self.x.append(item)

    def update(self, *args, **kwargs):
        
        return self.__dict__.update(*args, **kwargs)


def dictUpdate_getsame(oldD, newD):
    same = set()
    for ok,ov in oldD.items():
        for nk,nv in newD.items():
            if nk == ok and nv == ov:
                same.update([ok])
    return same

def confReload_updatePss():
   new conf =  json get $ user input file
   old conf = conf 
    protected = dictUpdate_getsame(confOld, confNew)
    for ps in pss:
        if ps name not in protected:
            ps.kill()
    LOG
    conf = new conf . copy 




def dict_update_k2(oldD, newD):
    same = []
    k = list(oldD.keys())
    k2 = list(newD.keys())
    fk = [*k, *k2]
    sk = set(fk)
    same = [k for k in sk if d[k] == d2[k]]
    return same

d = dict({"apple":10, "pear":20})
d2 = dict({"apple":'a', "pear":20, "futur":'z'})
"""
r = d["pear"] = 15
#print(r)
print(d, d.x)
d.update(d2)
print(d, d.x)
"""

z = dict_update_k1(d, d2)
z2 = dict_update_k1(d, d2)
print(z)
print(z2)
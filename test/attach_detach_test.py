

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


d = MyDict({"apple":10, "pear":20})
d2 = MyDict({"apple":'a', "pear":20, "futur":'z'})
r = d["pear"] = 15
#print(r)
print(d, d.x)
d.update(d2)
print(d, d.x)
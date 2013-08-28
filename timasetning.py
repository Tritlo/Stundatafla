class timi:
    def __init__(self,texti,litur):
        self.texti = texti
        self.litur = litur
        
    def __str__(self):
        return self.texti


class timasetning:

            
    def __init__(self,texti,litur):
        self.timar = [ timi(texti,litur) ]
        
    def add(self,texti,litur):
        self.timar.append(timi(texti,litur))

    def __getitem__(self,i):
        return self.timar[i]

    def __str__(self):
        strs = map(lambda t: str(t), self.timar)
        preBroken = any(map(lambda t: True if "<br />" in t else False,strs))
        if preBroken:
            return " ".join(strs)
        else:
            return "<br />".join(strs)

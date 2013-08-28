import string

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

    def getLabels(self):
        labels = map(lambda t: str(t).split()[:2], self.timar)
        joinF = lambda l: " ".join(l) if l[1][0] not in string.uppercase else l[0]
        labels = map(joinF,labels)
        return labels

    def changeColor(self,label, newColor):
        labels = self.getLabels()
        labels = map(lambda l: l.split()[0],labels)
        for i, l in enumerate(labels):
            if l == label:
                self.timar[i].litur = newColor
        

    def remove(self,label):
        labels = self.getLabels()
        index = labels.index(label)
        self.timar.pop(index)
        return len(self.timar) > 0

    def __getitem__(self,i):
        return self.timar[i]

    def __str__(self):
        strs = map(lambda t: str(t), self.timar)
        preBroken = any(map(lambda t: True if "<br />" in t else False,strs))
        if preBroken:
            return " ".join(strs)
        else:
            return "<br />".join(strs)

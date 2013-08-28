#!/usr/bin/python2
# -*- coding: utf-8 -*-
import util as u
import urllib2 as url
from StundatofluTable import table

class parser:

    def __init__(self,filename, litur = None):
        self.litur = litur
        if "http" in filename:
            f = url.urlopen(filename)
            self.html = f.read()
        else:
            with open(filename, "r") as f:
                self.html = f.read()

    def getListRep(self):
        spl = self.html.split("</table>")
        tab = spl[-2]
        tab = tab.split('<tr>')
        tab = "".join(tab).split('</tr>')[1:]
        tab.pop()
        tab = map(lambda row: "".join(row.split("<td><small>")).split("</small></td>")[1:],tab)
        tab = map(lambda row: map(lambda t: '' if t == '\n' else t.split('<small>')[-1],row),tab)
        return tab

        
    def toTable(self, tafla = None, title = None, heading = None):
        listrep = self.getListRep()
        if tafla is None:
            tafla = table(tafla,title,heading)
        places = u.getLocations(listrep, lambda t: True if t != "" else False)
        (x,y) = places[0]
        print "Fag: %s" % (listrep[x][y].split()[0],)
        if not self.litur:
            self.litur = raw_input("HTML litur: ")

        for (i,j) in places:
            tafla.addToTable(listrep[i][j],self.litur,i,j)
            
        return tafla
    @staticmethod
    def getLinks(filename):
        htm = url.urlopen(filename)
        htm = htm.read()
        htm = list(enumerate(htm.split("><")))
        links = filter(lambda t: True if "href=" in t[1] else False, htm)
        names = map(lambda l: (htm[l[0]+1][0],htm[l[0]+1][1].split("</span")[0]),links)
        names = map(lambda n: (n[0], n[1].split(">")[-1]), names) #.split(">")[-1]),links)

        flip = lambda (i,j): (j,i)
        names = map(flip,names)
        links = map(lambda l: (l[0],l[1].split('href="')[-1]),links)
        links = map(lambda l: (l[0],l[1][:len(l[1])-1]),links)
        linkDict = dict(links)

        names = map(lambda n: (n[0],linkDict[n[1]-1]), names)
        return dict(names)

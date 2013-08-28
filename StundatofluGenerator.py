#!/usr/bin/python2
# -*- coding: utf-8 -*-

import urllib2 as url
import sys
import codecs
from table import table

class parser:

    def __init__(self,filename):
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
        
    def toTable(self, tafla = None):
        listrep = self.getListRep()
        if tafla is None:
            tafla = table()
        locs = map(lambda t: list(enumerate(t)), listrep)
        locs = list(enumerate(map(lambda row: filter(lambda t: True if t[1] != "" else False,row), locs)))
        locs = filter(lambda t: t[1], locs)
        locs = map(lambda l: (l[0], map(lambda t: t[0], l[1])), locs)
        places = []
        for l in locs:
            for p in l[1]:
                places.append((l[0],p))

        (x,y) = places[0]
        print "Fag: %s" % (listrep[x][y].split()[0],)
        litur = raw_input("HTML litur: ")

        for (i,j) in places:
            tafla.addToTable(listrep[i][j],litur,i,j)
            
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

        
        
        

if __name__ == "__main__":
    args = sys.argv[1:]
    if '.p' in args[0]:
        tafla = table.load(args[0])
        dic = parser.getLinks("https://von.hi.is/von/stundat/haust/namskeid_toflur_haust.htm")
        args = map(lambda arg: dic[arg],args)
        for path in args[1:]:
            pars = parser(path)
            tafla = pars.toTable(tafla)
        tafla.save(args[0])
        with open(args[0][:len(args[0])-2] + '.html', 'w') as f:
            f.write(tafla.generatePage())
        
    else:
        dic = parser.getLinks("https://von.hi.is/von/stundat/haust/namskeid_toflur_haust.htm")
        args = map(lambda arg: dic[arg],args)
        pars = parser(args[0])
        tafla = pars.toTable()
        for path in args[1:]:
            pars = parser(path)
            tafla = pars.toTable(tafla)
        name = raw_input("Skrárnafn á output: ")
        tafla.save(name +'.p')
        with open(name + '.html', 'w') as f:
            f.write(tafla.generatePage())


               
           
           

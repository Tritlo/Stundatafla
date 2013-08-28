#!/usr/bin/python2
# -*- coding: utf-8 -*-
from optparse import OptionParser
from StundatofluTable import table
from StundatofluParser import parser
import StundatofluUtil as u
import string 
class editor:

    def __init__(self, table, courseDict):
        self.table = table
        self.courseDict = courseDict

    def getCourses(self):
        checkFunc = lambda t: True if t is not None else False
        locs = u.getLocations(self.table.tafla,lambda t: True if t is not None else False)
        timaDict = {}
        for (i,j) in locs:
            timar = self.table.tafla[i][j].timar
            for timi in timar:
                label = str(timi).split()[:2]
                if label[1][0] in string.uppercase:
                    label[1] = ""
                try:
                    fag = timaDict[label[0]]
                except KeyError:
                    timaDict[label[0]] = {}
                    fag = timaDict[label[0]]
                try:
                    fag[label[1]].append((i,j))
                except KeyError:
                    fag[label[1]] = [(i,j)]
                    
        return timaDict

    def remove(self):
        while True:
            print self.table
            zipDToStr = lambda vals: ", ".join(map(lambda (i, s): "%d. %s" %(i,s), vals))
            vals = lambda timar: zip(range(len(timar.keys())),timar.keys())
            timar = self.getCourses()
            print "Hvað fagi viltu breyta ('q' til að hætta)?"
            print zipDToStr(vals(timar))
            choice = raw_input("Fag: ")
            if choice == 'q':
                return self.table
            choice = int(choice)
            fag = dict(vals(timar))[choice]
            print "Hvað tíma viltu henda ('q' til að hætta)?"
            print zipDToStr(vals(timar[fag]))
            choice = raw_input("Tími: ")
            if choice == 'q':
                return self.table
            choice = int(choice)
            timi = dict(vals(timar[fag]))[choice]
            locs = timar[fag][timi]
            label = " ".join([fag,timi]) if timi != "" else fag
            res = map(lambda (i,j): self.table.tafla[i][j].remove(label),locs)
            for (i,j), r in zip(locs,res):
                if not r:
                    self.table.tafla[i][j] = None


    def changeColor(self):
        while True:
            zipDToStr = lambda vals: ", ".join(map(lambda (i, s): "%d. %s" %(i,s), vals))
            vals = lambda timar: zip(range(len(timar.keys())),timar.keys())
            timar = self.getCourses()
            print "Hvað fagi viltu breyta ('q' til að hætta)?"
            print zipDToStr(vals(timar))
            choice = raw_input("Fag: ")
            if choice == 'q':
                return self.table
            choice = int(choice)
            fag = dict(vals(timar))[choice]

            locs = []
            for val in timar[fag]:
                for loc in timar[fag][val]:
                    locs.append(loc)
                
            print "Hvað HTML lit viltu hafa ('q' til að hætta)?"
            litur = raw_input("HTML Litur: ")
            if litur == 'q':
                return self.table
                
            map(lambda (i,j): self.table.tafla[i][j].changeColor(fag,litur),locs)

    def addSubject(self):
        while True:
            print self.table
            zipDToStr = lambda vals: ", ".join(map(lambda (i, s): "%d. %s" %(i,s), vals))
            vals = lambda timar: zip(range(len(timar.keys())),timar.keys())
            timar = self.getCourses()
            print "Hvað fagi viltu bæta við ('q' til að hætta)?"
            fag = None
            while fag not in self.courseDict:
                fag = raw_input("Fag: ")
                if fag == 'q':
                    return self.table
                if fag in self.courseDict:
                    break
                else:
                    print "Fag ekki til, reyndu aftur ('q' til að hætta)"
            pars = parser(self.courseDict[fag])
            self.table = pars.toTable(self.table)
                  
            
    def changeTitle(self):
        print "Sláðu inn nýjan titil: "
        self.table.title = raw_input("Titill: ")

    def changeHeading(self):
        print "Sláðu inn nýja fyrirsögn: "
        self.table.title = raw_input("Fyrirsögn: ")
        
    def edit(self):
        vol = {"Fjarlægja tíma": self.remove, "Breyta lit": self.changeColor, "Bæta við fagi": self.addSubject, "Breyta titli": self.changeTitle, "Breyta fyrirsögn": self.changeHeading}
        while True:
            print "Hvað viltu gera?"
            zipDToStr = lambda vals: ", ".join(map(lambda (i, s): "%d. %s" %(i,s), vals))
            vals = lambda timar: zip(range(len(timar.keys())),timar.keys())
            print zipDToStr(vals(vol))
            choice = raw_input("Val: ")
            if choice == 'q':
                return self.table
            choice = int(choice)
            self.table = vol[dict(vals(vol))[choice]]()

            

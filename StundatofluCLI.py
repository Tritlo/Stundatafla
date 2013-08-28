#!/usr/bin/python2
# -*- coding: utf-8 -*-
import sys
from table import table

if __name__ == "__main__":
    if len(sys.argv) == 2:
        t = table.load(sys.argv[1])
        print t.generatePage()
        quit()
        
    fag = ""
    print "Velkomin í stundatöfluvélina"
    tafla = table()
    print tafla
    while fag != "q":
        print "Sladu inn fag til ad baeta vid, 'q' til ad haetta"
        fag = raw_input("Fag: ")
        if fag == 'q':
            print tafla
        else:
            fulltNafn = raw_input("Fullt nafn námskeiðs: ")
            adalkennari = raw_input("Kennari námskeiðs (upphafsstafir): ")
            litur = raw_input("HTML litur: ")
            print "Sláðu inn gerð tíma (f, d1, etc) og veldu tímasetningu, gerð 'q' til að hætta: "
            gerd = None
            while gerd != "q":
                gerd = raw_input("Gerð: ")
                if gerd == "q":
                    break
                lengd = raw_input("Fjoldi tima (1,2,etc): ")
                if lengd in '123456789':
                    lengd = int(lengd)
                else:
                    print "Vitlaus lengd, reyndu aftur"
                    continue
                kennari = raw_input("Kennari tíma (upphafsstafir), tómt ef aðalkennari: ")
                if kennari == "":
                    kennari = str(adalkennari)
                stadsetning = raw_input("Staðsetning: ")
                texti = fag + " " + gerd + " " + fulltNafn + " " + kennari + " " + stadsetning
                time, day = tafla.addToTable(texti,litur)
                i = 1
                while i < lengd:
                    time, day = tafla.addToTable(texti,litur, day = day, time= time+1)
                    i += 1
                print tafla
    print tafla.toHTML()
    tafla.save()
    vistaHtml = raw_input('Sláðu inn nafn á html skjali til að vista töflu í, tómt ef ekki á að vista: ')
    if vistaHtml != "":
        with open(vistaHtml, 'w') as f:
            f.write(tafla.generatePage())

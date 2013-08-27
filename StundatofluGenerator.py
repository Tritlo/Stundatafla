#!/usr/bin/python2
# -*- coding: utf-8 -*-
import cPickle as pickle
import sys

def printTable(tafla, terminal = True):
    if terminal:
        maxl=map(lambda t: max(map(lambda s: len(s[0]),t)),tafla)
        print
        maxl = max(maxl)
        addToString = lambda st: st[0] + (" "*(maxl-len(st[0].decode('utf-8'))))
        for t in tafla:
            taf = map(addToString,t)
            print ', '.join(taf)

def printHtml(tafla, title = None, heading = None):
    if title is None:
        title = raw_input("Titill síðu: ")
    if heading is None:
        heading = raw_input("Fyrirsögn töflu: ")
    header = """
<!doctype html>
<meta name="viewport" content="width=device-width, initial-scale=1,maximum-scale=10" charset="utf-8">
<head>
<title>%s</title>
</head>
<body>
	<h3 align="center">%s</h3>
    """ % (title,heading)
    footer = "</body></html>"
    str = header+tableToHTML(tafla) + footer
    print str

def tableToHTML(tafla):
    str = '<table width="100%%" border="1" cellspacing="0" cellpadding="3"><tbody>\n'
    dagar = map(lambda s: s[0], tafla[0])
    timar = map(lambda t: t[0][0], tafla)
    str += "<tr>\n"
    str += """<th width="10%%" align="center"></th>"""
    for d in dagar[1:]:
        str += """<th width="18%%" align="center">%s</th>""" % (d,)
    str += "</tr>\n"
    for row in tafla[1:]:
        str += addRow(row)
    str += "</tbody></table>\n"
    return str

def addRow(tableRow):
    time = tableRow[0][0]
    bgcol = tableRow[0][1]
    if bgcol is not None:
        str = '<tr bgcolor="%s">\n' % (bgcol,)
    else:
        str = "<tr>\n"
    for item in tableRow:
        text = item[0]
        color = item[1]
        if color is None:
            str += """<td><small>%s</small></td>\n""" % (text,)
        else:
            str += """<td bgcolor=%s><small>%s</small></td>\n""" % (color,text)
            
        
    str += "</tr>\n"
    return str

def saveTable(table, name = None):
    if name is None:
        name = raw_input("Skjal til að vista töflu í, tómt til að vista ekki: ")
        if name == '':
            return
    title = raw_input("Titill: ")
    heading = raw_input("Fyrirsögn: ")
    table = table, title, heading
    pickle.dump(table,open(name, "wb"))

def loadTable(name = None):
    if name is None:
        name = raw_input("Skjal til að opna: ")
    return pickle.load(open(name, "rb"))
    
def grunnTafla(last = None):
    dagar = ['','Mánudagur', 'Þriðjudagur', 'Miðvikudagur', 'Fimmtudagur', 'Föstudagur']
    timar = ['', '08:20-09:00', '09:10-09:50', '10:00-10:40', '10:50-11:30', '11:40-12:20', '12:30-13:10', '13:20-14:00', '14:10-14:50', '15:00-15:40', '15:50-16:30', '16:40-17:20', '17:30-18:10', '18:20-19:00', '19:10-20:00', '20:10-21:00']
    timar = zip(timar,[None for _ in range(len(timar))])
    dagar = zip(dagar,[None for _ in range(len(dagar))])
    timar[5] = timar[5][0],"#FFFFCC"
    
    timaShortcut = map(lambda t: "".join(t[0].split('-')[0].split(':')),timar)
    print "Hvenær byrjar síðasti tíminn þinn?"
    print 'Mögulegir tímar: '
    print timaShortcut
    while last is None:
        last = raw_input('Tími: ')
        if last in timaShortcut:
            timar = timar[:timaShortcut.index(last)+1]
        else:
            print "Vitlaus tími, reyndu aftur."
            last = None
    tafla = [[("",None) for i in range(len(dagar))] for j in range(len(timar))]
    tafla[0] = dagar
    for i in range(len(timar)):
        tafla[i][0] = timar[i]
    return tafla

def addToTable(tafla, toAdd = None, time = None, day = None):
    shortcuts = ['','ma','th','mi','fi','fo']
    dagaDict = dict(zip(shortcuts,range(len(shortcuts))))
    dagar = tafla[0]
    timar = [ t[0] for t in tafla]
    timaShortcut = map(lambda t: "".join(t[0].split('-')[0].split(':')),timar)
    timaDict = dict(zip(timaShortcut,range(len(timar))))
    while day is None:
        print "Mögulegir dagar"
        print shortcuts
        day = raw_input('Dagur: ')
        if day == "q":
            break
        if day in dagaDict:
            day = dagaDict[day]
        else:
            print "Vitlaus dagur, reyndu aftur eda 'q' til ad haetta"
            day = None
            
    if day == "q":
        return None
    while time is None:
        print "Mögulegir timar"
        print timaShortcut
        time = raw_input('Timi: ')
        if time == "q":
            break
        if time in timaDict:
            time = timaDict[time]
        else:
            print "Vitlaus timi, reyndu aftur eda 'q' til ad haetta"
            time = None
    if time == "q":
        return None

    if toAdd is None:
        texti = raw_input("Texti til ad baeta vid: "), None
    else:
        texti = toAdd
    if tafla[time][day][0] is not "":
        texti = tafla[time][day][0] + "\n<br>\n" + texti[0], texti[1]
    tafla[time][day] = texti
    return tafla, time, day

class timasetning:
    def __init__(self,fag, gerd, litur,kennari = None, stadsetning = None):
        self.fag = fag
        self.gerd = gerd
        self.litur = litur
        self.kennari = kennari
        self.stadsetning = stadsetning

    def __str__(self):
        str = self.fag
        if self.gerd:
            str += " " + self.gerd
        if self.kennari:
            str += " " + self.kennari
        else:
            str += " " + "NN"
        if self.stadsetning:
            str += " " + self.stadsetning
        
if __name__ == "__main__":
    if len(sys.argv) == 2:
        tafla, titill, fyrirsogn = loadTable(sys.argv[1])
        printHtml(tafla, titill, fyrirsogn)
        quit()
        
    fag = ""
    print "Velkomin í stundatöfluvélina"
    tafla = grunnTafla()
    printTable(tafla)
    while fag != "q":
        print "Sladu inn fag til ad baeta vid, 'q' til ad haetta"
        fag = raw_input("Fag: ")
        if fag == 'q':
            printTable(tafla)
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
                add = fag + " " + gerd + " " + fulltNafn + " " + kennari + " " + stadsetning, litur
                tafla, time, day = addToTable(tafla, toAdd = add )
                i = 1
                while i < lengd:
                    tafla, time, day = addToTable(tafla, toAdd = add, day = day, time= time+1)
                    i += 1
                printTable(tafla)
    saveTable(tafla)
    vistaHtml = raw_input('Sláðu inn nafn á html skjali til að vista töflu í, tómt ef ekki á að vista')
    if vistaHtml != "":
        title = raw_input("Titill síðu: ")
        heading = raw_input("Fyrirsögn töflu: ")
        with open(vistaHtml, 'w') as f:
            f.write(printHtml(tafla, title, heading))

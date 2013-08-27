#!/usr/bin/python2
# -*- coding: utf-8 -*-
import cPickle as pickle
import sys

class table:

    tafla = None
    title = None
    heading = None
    timar = ['08:20-09:00', '09:10-09:50', '10:00-10:40', '10:50-11:30', '11:40-12:20', '12:30-13:10', '13:20-14:00', '14:10-14:50', '15:00-15:40', '15:50-16:30', '16:40-17:20', '17:30-18:10', '18:20-19:00', '19:10-20:00', '20:10-21:00']
    dagar = ['Mánudagur', 'Þriðjudagur', 'Miðvikudagur', 'Fimmtudagur', 'Föstudagur']

    def __init__(self, table = None,title = None, heading = None):
        if table is None:
            self.tafla = self.grunnTafla()
        else:
            self.tafla = table
        if title is None:
            self.title = raw_input("Titill síðu: ")
        if heading is None:
            self.heading = raw_input("Fyrirsögn töflu: ")
        self.timar = self.timar[:len(self.tafla)]

    def timetable(self):
        dagar = [''] + self.dagar
        timar = [''] + self.timar
        new = [[None for _ in range(len(self.tafla[0])+1)] for _ in range(len(self.tafla) +1)]
        timar = zip(timar[:len(self.tafla)+1],[None for _ in range(len(self.tafla)+1)])
        if len(timar) > 5:
            timar[5] = timar[5][0],"#FFFFCC"
        new[0] = dagar
        for i in range(len(new)):
            new[i][0] = timar[i]
        for i,t in enumerate(self.tafla):
            for j,d in enumerate(t):
                new[i+1][j+1] = str(d)

        return new

    
    def __str__(self):
        tafla = self.timetable()
        maxl=map(lambda t: max(map(lambda s: len(str(s)),t)),tafla)
        maxl = max(maxl)
        addToString = lambda st: str(st) + (" "*(maxl-len(str(st).decode('utf-8'))))
        st = ""
        for t in tafla:
            t[0] = t[0][0]
            taf = map(addToString,t)
            st +=  '| '.join(taf) + '\n '
        return st

    def generatePage(self):
        header = """ <!doctype html>\n<meta name="viewport" content="width=device-width, initial-scale=1,maximum-scale=10" charset="utf-8">\n<head>\n<title>%s</title>\n</head>\n <body>\n<h3 align="center">%s</h3>\n """ % (self.title,self.heading)
        footer = "</body></html>"
        str = header+ self.toHTML() + footer
        return str

    def toHTML(self):
        st = '<table width="100%%" border="1" cellspacing="0" cellpadding="3"><tbody>\n'
        timetable = self.timetable()
        dagar = self.dagar
        timar = map(lambda t: t[0], timetable)[1:]
        st += "<tr>\n"
        st += """<th width="10%%" align="center"></th>"""
        for d in dagar:
            st += """<th width="18%%" align="center">%s</th>""" % (d,)
        st += "</tr>\n"

        def addHTMLRow(tableRow, time,bgcol ):
            if bgcol is not None:
                st = '<tr bgcolor="%s">\n' % (bgcol,)
            else:
                st = "<tr>\n"
            st += """<td><small>%s</small></td>\n""" % (time,)
            for item in tableRow:
                if item is None:
                    st += """<td><small></small></td>\n"""
                    continue
                text = str(item)
                color = item[-1].litur
                if color is None:
                    st += """<td><small>%s</small></td>\n""" % (text,)
                else:
                    st += """<td bgcolor=%s><small>%s</small></td>\n""" % (color,text)


            st += "</tr>\n"
            return st
        
        for i,row in enumerate(self.tafla):
            st += addHTMLRow(row, timar[i][0],timar[i][1])
        st += "</tbody></table>\n"
        return st


    def save(self, name = None):
        if name is None:
            name = raw_input("Skjal til að vista töflu í, tómt til að vista ekki: ")
            if name == '':
                return
        table = self.tafla, self.title, self.heading
        pickle.dump(table,open(name, "wb"))

    @staticmethod
    def load(name = None):
        if name is None:
            name = raw_input("Skjal til að opna: ")
        return pickle.load(open(name, "rb"))

    def grunnTafla(self,last = None):
        dagar = ['Mánudagur', 'Þriðjudagur', 'Miðvikudagur', 'Fimmtudagur', 'Föstudagur']
        timar = list(self.timar)
        timar = zip(timar,[None for _ in range(len(timar))])
        print len(timar)
        if len(timar) >= 5:
            timar[5] = timar[5][0],"#FFFFCC"

        timaShortcut = map(lambda t: "".join(t[0].split('-')[0].split(':')),timar)
        print "Hvenær byrjar síðasti tíminn þinn?"
        print 'Mögulegir tímar: '
        print timaShortcut
        while last is None:
            last = raw_input('Tími: ')
            if last in timaShortcut:
                timar = timar[:timaShortcut.index(last)]
            else:
                print "Vitlaus tími, reyndu aftur."
                last = None
        #tafla = [[("",None) for i in range(len(dagar))] for j in range(len(timar))]
        #tafla[0] = dagar
        #for i in range(len(timar)):
        #    tafla[i][0] = timar[i]
        tafla = [[None for _ in range(len(dagar))] for _ in range(len(timar))]
        return tafla

    def addToTable(self, toAdd = None, time = None, day = None, ):
        shortcuts = ['ma','th','mi','fi','fo']
        dagaDict = dict(zip(shortcuts,range(len(shortcuts))))
        dagar = self.dagar
        timar = [ t[0] for t in self.timetable()][1:]
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
            texti = raw_input("Texti til ad baeta vid: ")
            litur = raw_input("Litur: ")
            texti = timi(texti,litur)
        else:
            texti = toAdd

        return self.add(time, day, texti)

    def add(self, time, day, texti):
        self.tafla[time][day] = texti
        return time, day

class timi:
    def __init__(self,texti,litur):
        self.texti = texti
        self.litur = litur
        
    def __str__(self):
        return self.texti
        """
        str = self.fag
        if self.gerd:
            str += " " + self.gerd
        if self.kennari:
            str += " " + self.kennari
        else:
            str += " " + "NN"
        if self.stadsetning:
            str += " " + self.stadsetning
        """

class timasetning:

            
    def __init__(self,texti,litur):
        self.timar = [ timi(texti,litur) ]
        
    def add(self,texti,litur):
        self.timar.append(timi(text,litur))

    def __getitem__(self,i):
        return self.timar[i]

    def __str__(self):
        return "<br>".join(map(lambda t: str(t), self.timar))

        
if __name__ == "__main__":
    if len(sys.argv) == 2:
        tafla, titill, fyrirsogn = table.load(sys.argv[1])
        t = table(tafla,titill,fyrirsogn)
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
                timas = timasetning(texti,litur)
                add = timas
                time, day = tafla.addToTable(toAdd = add )
                i = 1
                while i < lengd:
                    time, day = tafla.addToTable(toAdd = add, day = day, time= time+1)
                    i += 1
                print tafla
    print tafla.toHTML()
    tafla.save()
    vistaHtml = raw_input('Sláðu inn nafn á html skjali til að vista töflu í, tómt ef ekki á að vista: ')
    if vistaHtml != "":
        with open(vistaHtml, 'w') as f:
            f.write(tafla.generatePage())

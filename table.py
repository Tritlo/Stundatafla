#!/usr/bin/python2
# -*- coding: utf-8 -*-
import cPickle as pickle
from timasetning import timasetning

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
        else:
            self.title = title
        if heading is None:
            self.heading = raw_input("Fyrirsögn töflu: ")
        else:
            self.heading = heading
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

    def lastNonEmptyRow(self):
        rows = map(lambda a: any(a), self.tafla)
        if not any(rows):
            last = len(rows)
        else:
            rows.reverse()
            last = rows.index(True)
            last = len(rows)-last +1
        return last
        
    def __str__(self):
        tafla = self.timetable()[:self.lastNonEmptyRow()]
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
        header = """<!doctype html>\n<meta name="viewport" content="width=device-width, initial-scale=1,maximum-scale=10" charset="utf-8">\n<head>\n<title>%s</title>\n</head>\n <body>\n<h3 align="center">%s</h3>\n""" % (self.title,self.heading)
        footer = "</body></html>"
        str = header+ self.toHTML() + footer
        return str

    def toHTML(self):
        st = '<table width="100%%" border="1" cellspacing="0" cellpadding="3"><tbody>\n'
        timetable = self.timetable()[:self.lastNonEmptyRow()]
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
        for i,row in enumerate(self.tafla[:self.lastNonEmptyRow()-1]):
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
        tafla, titill, fyrirsogn = pickle.load(open(name, "rb"))
        return table(tafla,titill,fyrirsogn)

    def grunnTafla(self,last = None):
        dagar = ['Mánudagur', 'Þriðjudagur', 'Miðvikudagur', 'Fimmtudagur', 'Föstudagur']
        timar = list(self.timar)
        timar = zip(timar,[None for _ in range(len(timar))])
        if len(timar) >= 5:
            timar[5] = timar[5][0],"#FFFFCC"

        timaShortcut = map(lambda t: "".join(t[0].split('-')[0].split(':')),timar)
        #print "Hvenær byrjar síðasti tíminn þinn?"
        #print 'Mögulegir tímar: '
        #print timaShortcut
        #while last is None:
        #    last = raw_input('Tími: ')
        #    if last in timaShortcut:
        #        timar = timar[:timaShortcut.index(last)+1]
        #    else:
        #        print "Vitlaus tími, reyndu aftur."
        #        last = None
        tafla = [[None for _ in range(len(dagar))] for _ in range(len(timar))]
        return tafla

    def addToTable(self, texti = None, litur = None, time = None, day = None, ):
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

        if texti is None:
            texti = raw_input("Texti til ad baeta vid: ")
        if litur is None:
            litur = raw_input("Litur: ")

        return self.add(time, day, texti, litur)

    def add(self, time, day, texti,litur):
        if self.tafla[time][day] is None:
            self.tafla[time][day] = timasetning(texti,litur)
        else:
            self.tafla[time][day].add(texti,litur)
        return time, day

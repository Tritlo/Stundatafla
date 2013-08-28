#!/usr/bin/python2
# -*- coding: utf-8 -*-
import urllib2 as url
from optparse import OptionParser
from StundatofluParser import parser
from StundatofluTable import  table
from StundatofluEditor import editor
import sys

if __name__ == "__main__":
    usage = "usage %prog [options] fag1 liturfag1 fag2 liturfag2 ..."
    optparser = OptionParser(usage=usage)
    optparser.add_option('-i', '--in', dest = "intable",
                         help ="Table to change or add to", metavar = "table.p")
    optparser.add_option('-o', '--out', dest = "outname",
                         help = "Name of output", metavar = "stundatafla")
    optparser.add_option('--title', dest = "title",
                         help = "Title of table", metavar = "Title")
    optparser.add_option( '--heading', dest = "heading",
                         help = "Heading of table", metavar = "Heading")
    
    optparser.add_option('-e', '--edit', dest = "editMode",
                         help = "Edit mode", action="store_true")
    
    (options, args) = optparser.parse_args()

    dic = parser.getLinks("https://von.hi.is/von/stundat/haust/namskeid_toflur_haust.htm")
    colors = []
    nargs = []
    for i, arg in enumerate(args):
        if i%2 == 0:
            nargs.append(arg)
        else:
            colors.append(arg)
    
    args = map(lambda arg: dic[arg],nargs)
    args = zip(args,colors)
    if options.intable:
        loadname = options.intable
        tafla = table.load(loadname)
        if options.editMode:
            ed = editor(tafla,dic)
            tafla = ed.edit()
        else:
            for (path,litur) in args:
                pars = parser(path,litur)
                tafla = pars.toTable(tafla)
        if not options.outname:
            tafla.save(loadname)
            with open(loadname[:len(loadname)-2] + '.html', 'w') as f:
                f.write(tafla.generatePage())
    else:
        if len(args) > 0:
            pars = parser(args[0][0], args[0][1])
            tafla = pars.toTable(title = options.title, heading = options.heading)
            for (path,litur) in args[1:]:
                pars = parser(path,litur)
                tafla = pars.toTable(tafla)
        if not options.outname:
            ed = editor(table(),dic)
            tafla = ed.edit()
            name = raw_input("Skrárnafn til að vista töflu og html: ")
            tafla.save(name +'.p')
            with open(name + '.html', 'w') as f:
                f.write(tafla.generatePage())
    
    if options.outname:
        tafla.save(options.outname +'.p')
        with open(options.outname + '.html', 'w') as f:
            f.write(tafla.generatePage())


               
           
           

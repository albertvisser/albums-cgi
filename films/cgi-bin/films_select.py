#! /usr/bin/env python
import cgi
import cgitb
cgitb.enable()
import films_padspecs
from select_main import Select

def main():
    form = cgi.FieldStorage()
    form_ok = 0
    sel_zoek = form.getvalue("selZoek", '')
    txt_zoek = form.getvalue("txtZoek", '')
    sorteren = form.getvalue("selSort", '')

    l = Select(sel_zoek, txt_zoek, sorteren)
    print "Content-Type: text/html"     # HTML is following
    print                               # blank line, end of headers
    for x in l.regels:
        print x

if __name__ == '__main__':
   main()

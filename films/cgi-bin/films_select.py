#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import cgi
import cgitb
cgitb.enable()
import sys
from codecs import getwriter
sys.stdout = getwriter("utf-8")(sys.stdout.buffer)
import films_padspecs
from select_main import Select

def main():
    form = cgi.FieldStorage()
    form_ok = 0
    sel_zoek = form.getvalue("selZoek", '')
    txt_zoek = form.getvalue("txtZoek", '')
    sorteren = form.getvalue("selSort", '')

    l = Select(sel_zoek, txt_zoek, sorteren)
    print("Content-Type: text/html\n")     # HTML is following
    for x in l.regels:
        print(x)

if __name__ == '__main__':
   main()

#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import cgi
import cgitb
cgitb.enable()
import sys
from codecs import getwriter
sys.stdout = getwriter("utf-8")(sys.stdout.buffer)
import films_padspecs
from detail_main import Detail

def main():
    form = cgi.FieldStorage()
    form_ok = 0
    print("Content-Type: text/html\n")     # HTML is following

    film_id = form.getfirst("selFilms", -1)
    sel_zoek = form.getfirst("selZoek", '')
    txt_zoek = form.getfirst("txtZoek", '')
    sorteren = form.getfirst("selSort", '')
    wijzig = form.getfirst("hWijzig", 0)

    l = Detail(film_id, wijzig, sel_zoek, txt_zoek, sorteren)
    for x in l.regels:
        print(x)

if __name__ == '__main__':
   main()


#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import cgi
import cgitb
cgitb.enable()
import sys
from codecs import getwriter
sys.stdout = getwriter("utf-8")(sys.stdout.buffer)
import muziek_ini
from select_main import Select

def main():
    form = cgi.FieldStorage()
    form_ok = 0
    h =  Select()
    sel_artiest = form.getfirst("selArtiest", None)
    sel_type = form.getfirst("hType", None)
    if "hStudio" in form:
        h.set_arg('albumtype', 'studio')
        selzoek = form.getfirst("selZoekS", None)
        if selzoek is not None and selzoek != 'None':
            if selzoek == "artiest":
                h.set_arg('tZoek', sel_artiest)
            else:
                h.set_arg('tZoek', form.getfirst("txtZoekS", None))
            h.set_arg('sZoek', selzoek)
        selsort = form.getfirst("selSortS", None)
        if selsort is not None:
            h.set_arg('sorteren', selsort)
    elif "hLive" in form:
        h.set_arg('albumtype', 'live')
        selzoek = form.getfirst("selZoekL", None)
        if selzoek is not None and selzoek != 'None':
            if selzoek == "artiest":
                h.set_arg('tZoek', sel_artiest)
            else:
                h.set_arg('tZoek', form.getfirst("txtZoekL", None))
            h.set_arg('sZoek',selzoek)
        selsort = form.getfirst("selSortL", None)
        if selsort is not None:
            h.set_arg('sorteren', selsort)
    #-- toevoeging o.b.v. selector andere artiest op selectiescherm
    elif sel_artiest:
        h.set_arg('albumtype', sel_type)
        h.set_arg('sZoek', form.getfirst("hZoek", None))
        h.set_arg('tZoek', sel_artiest)
        h.set_arg('sorteren', form.getfirst("hSort", None))
    #-- einde toevoeging
    elif sel_type:
        h.set_arg('albumtype', sel_type)
        h.set_arg('sZoek', form.getfirst("hSZoek", None))
        h.set_arg('tZoek', form.getfirst("hTZoek", None))
        h.set_arg('sorteren', form.getfirst("hSort", None))
    h.go()
    print("Content-Type: text/html\n")     # HTML is following
    for x in h.regels:
        try:
            print(x)
        except UnicodeEncodeError:
            print(x.encode("utf-8"))

if __name__ == '__main__':
	main()

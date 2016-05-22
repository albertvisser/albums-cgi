#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import cgi
import cgitb
cgitb.enable()
import sys
from codecs import getwriter
sys.stdout = getwriter("utf-8")(sys.stdout.buffer)
import muziek_ini
from meldfout import meldfout
from detail_main import Detail

def main():
    form = cgi.FieldStorage()
    form_ok = True
    foutregel = ''
    albumtype = form.getfirst("hAlbumType", '')
    albumid = form.getfirst("hAlbumId", None)
    wijzigO = True # voor zover nodig
    if albumid is None:
        foutregel = 'Geen albumid opgegeven'
    elif albumtype == '':
        foutregel = "Geen album type gekozen"
    else:
        dm = Detail(albumtype, wijzigO, albumid)
        opn_id = form.getfirst('hOpnId', None)
        if opn_id is None:
            foutregel = "Geen opname nummer opgegeven"
        else:
            dm.opnameid = int(opn_id)
            dm.opnameoms = form.getfirst('txtOpn{}'.format(opn_id), '')
            h = dm.wijzig() # albumtype,albumid

    print("Content-Type: text/html\n")     # HTML is following
    if foutregel != '':
        print(meldfout(foutregel, "Magiokis Muziek!"))
        cgi.print_form(form)
    else:
        dm.toon()
        for x in dm.regels:
            print(x)

if __name__ == '__main__':
	main()

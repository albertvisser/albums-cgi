#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import cgi
import cgitb
cgitb.enable()
import sys
from codecs import getwriter
sys.stdout = getwriter("utf-8")(sys.stdout.buffer)
import muziek_ini
from start_main import start

def main():

    form = cgi.FieldStorage()
    meld = form.getfirst("fout", "&nbsp;")

    print("Content-Type: text/html\n")   # HTML is following
    ## print(''.join([str(x.encode('utf-8')) for x in start(meld)]))
    ## regels = ["hallo", "daar"]
    regels = start(meld)
    for x in regels:
        try:
            print(x)
        except UnicodeEncodeError:
            print(x.encode("utf-8"))

if __name__ == '__main__':
    main()


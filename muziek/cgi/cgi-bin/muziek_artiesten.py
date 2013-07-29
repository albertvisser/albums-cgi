#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import cgi
import cgitb
cgitb.enable()
import sys
from codecs import getwriter
sys.stdout = getwriter("utf-8")(sys.stdout.buffer)
import muziek_ini
from artiesten_main import Artiesten, Fout

def main():
    form = cgi.FieldStorage()
    args = {"editEntry": False}
    if "hNieuw" in form:
        args["editEntry"] = True
    test = form.getfirst("edit", None)
    if test is not None:
        args["editEntry"] = True
        args["selId"] = test
    test = form.getfirst("after", None)
    if test is not None:
        args["editEntry"] = True
        args["afterId"] = test
        args["sSort"] = form.getfirst("sort", None)
    print("Content-Type: text/html\n")     # HTML is following
    try:
        m = Artiesten(args)
    except Fout as meld:
        print(meld)
    else:
        for x in m.regels:
            try:
                print(x)
            except UnicodeEncodeError:
                print(x.encode("utf-8"))

if __name__ == '__main__':
    main()


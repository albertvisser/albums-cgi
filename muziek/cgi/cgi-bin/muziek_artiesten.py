#! /usr/bin/env python
import cgi
import cgitb
cgitb.enable()
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
    print "Content-Type: text/html"     # HTML is following
    print                               # blank line, end of headers
    try:
        m = Artiesten(args)
    except Fout as meld:
        print meld
    else:
        for x in m.regels:
            print x

if __name__ == '__main__':
    main()


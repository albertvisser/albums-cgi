#! /usr/bin/env python
import cgi
import cgitb
cgitb.enable()
import muziek_ini
from start_main import start

def main():

    form = cgi.FieldStorage()
    meld = form.getfirst("fout", "&nbsp;")

    print "Content-Type: text/html"     # HTML is following
    print                               # blank line, end of headers
    regels = start(meld)
    for x in regels:
        print x

if __name__ == '__main__':
    main()


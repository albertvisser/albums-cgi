import cgi
import sys
from films_padspecs import *
from films_select_main import select_main

def main():
    form = cgi.FieldStorage()
    form_ok = 0
    sZoek = ''
    tZoek = ''
    sorteren = ''
    if form.has_key("selZoek"):
        sZoek = form["selZoek"].value
    if form.has_key("txtZoek"):
        tZoek = form["txtZoek"].value
    if form.has_key("selSort"):
        sorteren = form["selSort"].value

    l = select_main(sZoek,tZoek,sorteren)
    print "Content-Type: text/html"     # HTML is following
    print                               # blank line, end of headers
    for x in l.regels:
        print x

if __name__ == '__main__':
   main()

import cgi
import sys
from films_padspecs import *
from meld_fout import meldfout
from films_detail_main import detail_main

def main():
    form = cgi.FieldStorage()
    form_ok = 0
    print "Content-Type: text/html"     # HTML is following
    print                               # blank line, end of headers

    if form.has_key("selFilms"):
        filmid = form["selFilms"].value
    else:
        filmid = -1
    if form.has_key("wijzigO"):
        wijzigO = form["hWijzig"].value
    else:
        wijzigO = 0

    l = detail_main(filmid,wijzigO)
    for x in l.regels:
        print x

if __name__ == '__main__':
   main()


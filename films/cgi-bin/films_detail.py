#! /usr/bin/env python
import cgi
import cgitb
cgitb.enable()
import films_padspecs
from detail_main import Detail

def main():
    form = cgi.FieldStorage()
    form_ok = 0
    print "Content-Type: text/html"     # HTML is following
    print                               # blank line, end of headers

    film_id = form.getfirst("selFilms", -1)
    wijzig = form.getfirst("hWijzig", 0)

    l = Detail(film_id, wijzig)
    for x in l.regels:
        print x

if __name__ == '__main__':
   main()


import cgi
import sys
from adr_padspecs import *
sys.path.append(progpad) # waar de eigenlijke programmatuur staat
from adres_select_main import select

def main():
    form = cgi.FieldStorage()
    form_ok = 0
    selId = ''
    editEntry = 0
    if form.has_key("edit"):
        editEntry = 1
        selId = form["edit"].value
    l = select("ans",editEntry,selId)
    if editEntry:
        f = file(htmlpad + "temp.html","w")
        for x in l:
            f.write("%s\n" % x)
        f.close()
        print "Content-Type: text/html"     # HTML is following
        print "Location: http://adr.pythoneer.nl/temp.html#wijzigdeze"
        print                               # blank line, end of headers
    else:
        print "Content-Type: text/html"     # HTML is following
        print                               # blank line, end of headers
        for x in l:
            print x

if __name__ == '__main__':
    main()


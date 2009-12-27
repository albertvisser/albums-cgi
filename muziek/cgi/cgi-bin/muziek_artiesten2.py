import cgi
import muziek_ini
from muziek_artiesten_main import *

def main():
    form = cgi.FieldStorage()
    args = {}
    if form.has_key("hId"):
       args["selId"] = form["hId"].value
    if form.has_key("tnaam"):
       args["hNaam"] = form["tnaam"].value
    if form.has_key("tstraat"):
       args["hSort"] = form["tsort"].value
    try:
        m = artiest_wijzig(args)
    except Fout,meld:
        print "Content-Type: text/html"     # HTML is following
        print                               # blank line, end of headers
        print meld
    else:
        m = artiesten_main(args)
        print "Content-Type: text/html"     # HTML is following
        print                               # blank line, end of headers
        for x in m.regels:
            print x

if __name__ == '__main__':
    main()


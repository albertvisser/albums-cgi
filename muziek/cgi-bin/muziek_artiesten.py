import cgi
import muziek_ini
from muziek_artiesten_main import *

def main():
    form = cgi.FieldStorage()
    #~ print "Content-Type: text/html"     # HTML is following
    #~ print                               # blank line, end of headers
    #~ print "<html>"
    #~ print "<head></head>"
    #~ print "<body>"
    #~ keys = form.keys()
    #~ keys.sort()
    #~ print
    #~ print "<H3>Form Contents:</H3>"
    #~ if not keys:
        #~ print "<P>No form fields."
    #~ print "<DL>"
    #~ for key in keys:
        #~ print "<DT>" + cgi.escape(key) + ":",
        #~ value = form[key]
        #~ print "<i>" + cgi.escape(`type(value)`) + "</i>"
        #~ print "<DD>" + cgi.escape(`value`)
    #~ print "</DL>"
    #~ print
    #~ print "</body></html>"
    #~ return
    args = {"editEntry": False}
    if form.has_key("hNieuw"):
        args["editEntry"] = True
    if form.has_key("edit"):
        args["editEntry"] = True
        args["selId"] = form["edit"].value
    if form.has_key("after"):
        args["editEntry"] = True
        args["afterId"] = form["after"].value
        args["sSort"] = form["sort"].value
    try:
        m = artiesten_main(args)
    except Fout,meld:
        print "Content-Type: text/html"     # HTML is following
        print                               # blank line, end of headers
        print meld
    else:
        print "Content-Type: text/html"     # HTML is following
        print                               # blank line, end of headers
        for x in m.regels:
            print x

if __name__ == '__main__':
    main()


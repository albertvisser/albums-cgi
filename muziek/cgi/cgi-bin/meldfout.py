def meldfout(melding,header="",css=""):
    # fout melden
    print "Content-Type: text/html"     # HTML is following
    print                               # blank line, end of headers
    print "<html>"
    print "<head>"
    if css != "":
        print ('<link rel="stylesheet" href="%s" type="text/css">' % css)
    print "</head>"
    if header != "":
        print ('<h1><a>%s</a></h1>' % header)
        print '<hr />'
    print ("<body>%s</body>" % melding)
    print "</html>"
    return

def main():
    m = "Dit is een foutmelding"
##    meldfout(m)
    h =  "Header Tekst"
##    meldfout(m,h)
    s = "http://films.pythoneer.nl/films.css"
    meldfout(m,h,s)
    return

if __name__ == '__main__':
    main()

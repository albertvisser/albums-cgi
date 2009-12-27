import cgi
import muziek_ini
from muziek_start_main import start_main

def main():

    meld = "&nbsp;"
    form = cgi.FieldStorage()
    if form.has_key("fout"):
        meld = form["fout"].value

    print "Content-Type: text/html"     # HTML is following
    print                               # blank line, end of headers
    l = start_main(meld)
    for x in l.regels:
        print x

if __name__ == '__main__':
    main()


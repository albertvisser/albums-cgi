def meldfout(melding,header="",css=""):
    # fout melden
    lines = []
    lines.append("<html>")
    lines.append("<head>")
    if css != "":
        lines.append('<link rel="stylesheet" href="%s" type="text/css">' % css)
    lines.append("</head>")
    if header != "":
        lines.append('<h1><a>%s</a></h1>' % header)
        lines.append('<hr />')
    lines.append("<body>%s</body>" % melding)
    lines.append("</html>")
    return lines

def main():
    m = "Dit is een foutmelding"
##    meldfout(m)
    h =  "Header Tekst"
##    meldfout(m,h)
    s = "http://papa/films/films.css"
    l = meldfout(m,h,s)
    for x in l.lines:
        print x
    return

if __name__ == '__main__':
    main()

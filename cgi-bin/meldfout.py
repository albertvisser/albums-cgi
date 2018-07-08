# -*- coding: utf-8 -*-

def meldfout(melding, header="", css=""):
    # fout melden
    template = "<html><head>{}</head><body>{}{}</body></html>"
    if not css:
        css = "http://muziek.lemoncurry.nl/muziek.css"
    css = '<link rel="stylesheet" href="%s" type="text/css">' % css
    if header != "":
        header = '<h1><a>%s</a></h1><hr />' % header
    return template.format(css, header, melding)

def main():
    m = "Dit is een foutmelding"
##    meldfout(m)
    h =  "Header Tekst"
##    meldfout(m,h)
    s = "http://films.pythoneer.nl/films.css"
    print(meldfout(m,h,s))
    return

if __name__ == '__main__':
    main()

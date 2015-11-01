import os
HERE = os.path.dirname(__file__)
xmlpad = os.path.join(HERE, "data")
htmlpad = os.path.join(os.path.dirname(os.path.dirname(HERE)),
    "www/lemoncurry/films/")
httppad = "http://www.lemoncurry.nl/films/"
import sys
sys.path.append(xmlpad) # pad naar de gegevens

def meldfout(melding, header="", css=""):
    lines = []
    lines.append("<html>")
    lines.append("<head>")
    if css:
        lines.append('<link rel="stylesheet" href="%s" type="text/css">' % css)
    lines.append("</head>")
    if header:
        lines.append('<h1><a>%s</a></h1>' % header)
        lines.append('<hr />')
    lines.append("<body>%s</body>" % melding)
    lines.append("</html>")
    return lines


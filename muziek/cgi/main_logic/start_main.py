import globals
from artiest import artiestenlijst

def start(meld):
    regels = []
    with open("%sstart.html" % globals.htmlpad) as fh:
        for x in fh:
            x = x.rstrip()
            xh = x.split()
            if xh[0] == "<!--":
                if xh[1] == "kop":
                    regels += globals.kop("start")
                elif xh[1] == "artiest":
                    for y in artiestenlijst():
                        regels.append(" ".join(xh[-3:-1]) % (y[0],y[1]))
                elif xh[1] == "fout":
                    regels.append(" ".join(xh[-4:-1]) % meld)
            else:
                regels.append(x)
    return regels

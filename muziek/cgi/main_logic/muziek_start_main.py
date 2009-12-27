import muziek_globals
htmlpad = muziek_globals.htmlpad
from muziek_artiest import ArtiestenLijst

class start_main:
    def __init__(self,meld):
        self.regels = []
        dh = ArtiestenLijst()
        fh = open("%sstart.html" % htmlpad)
        for x in fh.readlines():
            xh = x[:-1].split()
            if xh[0] == "<!--":
                if xh[1] == "kop":
                    h = muziek_globals.kop("start")
                    for y in h.regels:
                        self.regels.append(y)
                elif xh[1] == "artiest":
                    for y in dh.Namen:
                        self.regels.append('					 <option value="%s">%s</option>' % (y[0],y[1]))
                elif xh[1] == "fout":
                    self.regels.append('  <span class="mess">%s</span><br />' % meld)
            else:
                self.regels.append(x[:-1])
        fh.close()

if __name__ == '__main__':
    h = start_main("Er is iets misgegaan - nee hoor, grapje")
    for x in h.regels:
        print x

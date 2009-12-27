import string
from films_globals import *
from Films import FilmList
from meld_fout import meldfout

class select_main:
    def __init__(self,sZoek,tZoek,sorteren=''):
        self.sZoek = sZoek
        self.tZoek = tZoek
        self.sorteren = sorteren
        self.regels = []
        list = ['titel']
        if self.sorteren == 'loc':
            list.append('loc')
        if self.sZoek != "None":
            selection = {}
            selection[self.sZoek] = tZoek
            self.fl = FilmList(list, selection)
        else:
            self.fl = FilmList(list)
        if len(self.fl.Items) == 0:
            f = ('Geen films gevonden met "%s" in "%s"' % (tZoek, sZoek))
            for x in meldfout(f,"Magiokis Films!","%sfilms.css" % httppad):
                self.regels.append(x)
        else:
            self.maakselect()

    def maakselect(self):
        #-- de list sorteren
        sortList = []
        sl = []
        if self.sorteren == 'loc':
            for x in self.fl.Items:
                if x[1] != None:
                    y = x[1] + ";#; " + x[2] + ";#;" + x[0]
                    sortList.append(y)
            sortList.sort()
            for x in sortList:
                y = x.split(";#;")
                sl.append(y)
        elif self.sorteren == 'titel':
            for x in self.fl.Items:
                y = x[1] + ";#;" + x[0]
                sortList.append(y)
            sortList.sort()
            for x in sortList:
                y = x.split(";#;")
                sl.append(y)
        else:
            for x in self.fl.Items:
                y = [x[1], x[0]]
                sl.append(y)

        fh = open("%sselect.html" % htmlpad)
        for x in fh.readlines():
            if x == "<!-- selectie -->\n":
                if self.sZoek == 'None':
                    h = '  Geen selectie;'
                else:
                    h = ('  Selectie op %s: %s;' % (self.sZoek, self.tZoek))
                if self.sorteren == 'geen':
                    h = h + " geen sortering"
                else:
                    h = h + (' sortering op %s' % self.sorteren)
                self.regels.append(h)
            elif x == "<!-- options -->\n":
                if self.sorteren == 'loc':
            #        fl.Items bestaat uit id, titel en loc
                    for y in sl:
                        self.regels.append('  <option value="%s">%s %s</option>' % (y[2],y[0],y[1]))
                else:
            #        fl.Items bestaat uit id en titel
                    for y in sl:
                        self.regels.append('  <option value="%s">%s</option>' % (y[1],y[0]))
            else:
                self.regels.append(x[:-1])
        fh.close

if __name__ == '__main__':
    sZoek = 'None'
    tZoek = ''
    sorteren = ""
    s = select_main(sZoek,tZoek,sorteren)
    for x in s.regels:
        print x

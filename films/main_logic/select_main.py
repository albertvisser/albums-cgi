import common
from films import FilmList

class Select:
    def __init__(self, sel_zoek, txt_zoek, sorteren=''):
        self.sel_zoek = sel_zoek
        self.txt_zoek = txt_zoek
        self.sorteren = sorteren
        self.regels = []
        list = ['titel']
        if self.sorteren == 'loc':
            list.append('loc')
        if self.sel_zoek == "alles":
            self.fl = FilmList(list)
        else:
            self.fl = FilmList(list, {sel_zoek: txt_zoek})
        if len(self.fl.items) == 0:
            f = ('Geen films gevonden met "%s" in "%s"' % (txt_zoek, sel_zoek))
            for x in common.meldfout(f, "Magiokis Films!",
                    "%sfilms.css" % common.httppad):
                self.regels.append(x)
        else:
            self.maakselect()

    def maakselect(self):
        #-- de list sorteren
        if self.sorteren == 'loc':
            sort_list = [(x[1], x[2], x[0]) for x in self.fl.items]
            sort_list.sort()
        elif self.sorteren == 'titel':
            sort_list = [(x[1], x[0]) for x in self.fl.items]
            sort_list.sort()
        else:
            sort_list = [(x[1], x[0]) for x in self.fl.items]
        sl = sort_list

        with open("%sselect.html" % common.htmlpad) as fh:
            for x in fh:
                x = x.rstrip()
                if x == "<!-- selectie -->":
                    if self.sel_zoek == 'alles':
                        h = '  Geen selectie;'
                    else:
                        h = ('  Selectie op %s: %s;' % (self.sel_zoek, self.txt_zoek))
                    if self.sorteren == 'geen':
                        h = h + " geen sortering"
                    else:
                        h = h + (' sortering op %s' % self.sorteren)
                    self.regels.append(h)
                elif x == "<!-- options -->":
                    if self.sorteren == 'loc':
                #        fl.Items bestaat uit id, titel en loc
                        for y in sl:
                            self.regels.append('  <option value="%s">%s %s</option>' % (y[2],y[0],y[1]))
                    else:
                #        fl.Items bestaat uit id en titel
                        for y in sl:
                            self.regels.append('  <option value="%s">%s</option>' % (y[1],y[0]))
                else:
                    self.regels.append(x)

import common
from films import Film

class Detail:
    def __init__(self, film_id=-1, wijzig=0, sel_zoek='', txt_zoek='', sorteren=''):
        self.film_id = film_id
        self.wijzig = wijzig
        self.sel_zoek = sel_zoek
        self.txt_zoek = txt_zoek
        self.sorteren = sorteren
        self.regels = []
        mt = "Magiokis Films!"
        ms = ("%sfilms.css" % common.httppad)
        if self.film_id == -1:
            for x in common.meldfout("Geen film-id opgegeven", mt, ms):
                self.regels.append(x)
        else:
            self.sh = Film(self.film_id)
            self.sh.read()
            if not self.sh.found:
                for x in common.meldfout("Film-gegevens niet aanwezig", mt, ms):
                    self.regels.append(x)
            else:
                self.maakdetail()

    def maakdetail(self):
        with open("%sdetail.html" % common.htmlpad) as fh:
            for x in fh:
                x = x.rstrip()
                if x.startswith("<!--"):
                    y = x[4:-4].split(None, 1)
                    if y[0] == "titel":
                        self.regels.append(y[1] % self.sh.titel)
                    elif y[0] == "van":
                        self.regels.append(y[1] % self.sh.van)
                    elif y[0] == "jaar":
                        self.regels.append(y[1] % self.sh.jaar)
                    elif y[0] == "met":
                        self.regels.append(self.sh.met)
                    elif y[0] == "over":
                        self.regels.append(self.sh.over)
                    elif y[0] == "loc":
                        self.regels.append(y[1] % self.sh.loc)
                    elif y[0] == "duur":
                        self.regels.append(y[1] % self.sh.duur)
                    elif y[0] == "wijzigO":
                        hlp = '0' if self.wijzig != 1 else '1'
                        self.regels.append(y[1] % hlp)
                elif 'radio' in x:
                    hlp = ''
                    if (self.sh.soort and self.sh.soort in x) or (self.sh.taal and
                            self.sh.taal in x):
                        hlp = 'checked="checked"'
                    self.regels.append(x.format(hlp))
                elif 'selFilms' in x:
                    self.regels.append(x.format(self.film_id))
                elif 'selZoek' in x:
                    self.regels.append(x.format(self.sel_zoek, self.txt_zoek,
                        self.sorteren))
                else:
                    self.regels.append(x)

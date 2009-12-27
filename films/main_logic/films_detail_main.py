import string
from films_globals import *
from Films import Film
from meld_fout import meldfout

class detail_main:
    def __init__(self,filmid=-1,wijzigO=0):
        self.filmid = filmid
        self.wijzigO = wijzigO
        self.regels = []
        mt = "Magiokis Films!"
        ms = ("%sfilms.css" % httppad)
        if self.filmid == -1:
            for x in meldfout("Geen film-id opgegeven",mt,ms):
                self.regels.append(x)
        else:
            self.sh = Film(self.filmid)
            self.sh.read()
            if not self.sh.found:
                for x in meldfout("Film-gegevens niet aanwezig",mt,ms):
                    self.regels.append(x)
            else:
                self.maakdetail()

    def maakdetail(self):
        fh = open("%sdetail.html" % htmlpad)
        for x in fh.readlines():
            if x[0:4] == "<!--":
                if x[5:10] == "titel":
                    # <!-- titel     <input type="text" name="titel" size="60" maxlength="80" value="%s"/><br /> -->
                    p = x[11:]
                    p = p[:-4]
                    self.regels.append(p % self.sh.Titel)
                elif x[5:8] == "van":
                    # <!-- van     <input type="text" name="van" size="40" maxlength="80" value="%s"/> -->
                    p = x[9:]
                    p = p[:-4]
                    self.regels.append(p % self.sh.Van)
                elif x[5:9] == "jaar":
                    # <!-- jaar     <input type="text" name="jaar" size="10" maxlength="10" value="%s"/><br /> -->
                    p = x[10:]
                    p = p[:-4]
                    self.regels.append(p % self.sh.Jaar)
                elif x[5:8] == "met":
                    # <!-- met -->
                    self.regels.append(self.sh.Met)
                elif x[5:9] == "over":
                    # <!-- over -->
                    self.regels.append(self.sh.Over)
                elif x[5:8] == "loc":
                    # <!-- loc     <input type="text" name="loc" size="10" maxlength="10" value="%s"/> -->
                    p = x[9:]
                    p = p[:-4]
                    self.regels.append(p % self.sh.Loc)
                elif x[5:9] == "duur":
                    # <!-- duur     <input type="text" name="duur" size="10" maxlength="10" value="%s" /> min.<br /> -->
                    p = x[10:]
                    p = p[:-4]
                    self.regels.append(p % self.sh.Duur)
                elif x[5:12] == "wijzigO":
                    # <!-- wijzigO <input type="hidden" name="hWijzig" value="%s"> -->
                    p = x[13:]
                    p = p[:-4]
                    if self.wijzigO != 1:
                        self.regels.append(p % "0")
                    else:
                        self.regels.append(p % "1")
            else:
                self.regels.append(x[:-1])

if __name__ == '__main__':
    filmid = 10
    wijzigO = 0
    l = detail_main(filmid,wijzigO)
    for x in l.regels:
        print x

from adres_globals import *
from adressen import Naw

class adres:
    def __init__(self,id):
        self.Id = id
        self.wijzignaam = False
        self.wijzigstraat = False
        self.wijzigplaats = False
        self.wijzigpostcode = False
        self.wijzigtelefoon = False
        self.wijziggeboren = False
        self.wijzigemail = False
        self.Naam = ""
        self.Straat = ""
        self.Plaats = ""
        self.Postcode = ""
        self.Telefoon = ""
        self.Geboren = ""
        self.Email = ""

    def setAttr(self,x,y):
        ok = True
        if x == "naam":
            self.Naam = y
            self.wijzignaam = True
        elif x == "straat":
            self.Straat = y
            self.wijzigstraat = True
        elif x == "plaats":
            self.Plaats = y
            self.wijzigplaats = True
        elif x == "postcode":
            self.Postcode = y
            self.wijzigpostcode = True
        elif x == "telefoon":
            self.Telefoon = y
            self.wijzigtelefoon = True
        elif x == "geboren":
            self.Geboren = y
            self.wijziggeboren = True
        elif x == "email":
            self.Email = y
            self.wijzigemail = True
        else:
            ok = False
        return ok

class wijzig:
    def __init__(self,soort,adres):
        if soort == "school":
            from adres_globals import school_xmldoc
            if adres.Id == "0":
                ln = Naw(school_xmldoc,0)
                adres.Id = ln.Id
            ih = Naw(school_xmldoc,adres.Id)
        elif soort == "ans":
            from adres_globals import ans_xmldoc
            if adres.Id == "0":
                ln = Naw(ans_xmldoc,0)
                adres.Id = ln.Id
            ih = Naw(ans_xmldoc,adres.Id)
        else:
            self.ok = False
        self.ok = True
        if self.ok:
            hwijzig = 0
            ih.read()
            if adres.wijzignaam:
                if ih.found and adres.Naam != ih.Naam or not ih.found:
                    ih.wijzigNaam(adres.Naam)
                    hwijzig = 1
            if adres.wijzigstraat:
                if ih.found and adres.Straat != ih.Straat or not ih.found:
                    ih.wijzigStraat(adres.Straat)
                    hwijzig = 1
            if adres.wijzigpostcode:
                if ih.found and adres.Postcode != ih.Postcode or not ih.found:
                    ih.wijzigPostcode(adres.Postcode)
                    hwijzig = 1
            if adres.wijzigplaats:
                if ih.found and adres.Plaats != ih.Plaats or not ih.found:
                    ih.wijzigPlaats(adres.Plaats)
                    hwijzig = 1
            if adres.wijzigtelefoon:
                if ih.found and adres.Telefoon != ih.Telefoon or not ih.found:
                    ih.wijzigTelefoon(adres.Telefoon)
                    hwijzig = 1
            if adres.wijziggeboren:
                if ih.found and adres.Geboren != ih.Geboren or not ih.found:
                    ih.wijzigGeboren(adres.Geboren)
                    hwijzig = 1
            if adres.wijzigemail:
                if ih.found and adres.Email != ih.Email or not ih.found:
                    ih.wijzigEmail(adres.Email)
                    hwijzig = 1
            if hwijzig:
                ih.write()

if __name__ == '__main__':
    test = "ans"
    h = adres("27")
    h.setAttr("naam","iemand")
    h.setAttr("straat","Ergens")
    h.setAttr("postcode","ja, daar")
    h.setAttr("plaats","op die plek")
    h.setAttr("telefoon","42")
    h.setAttr("geboren","ooit")
    h.setAttr("email","x@y.com")
    w = wijzig(test,h)
    if w.ok:
        print "item al dan niet gewijzigd"
    else:
        print "fout opgetreden"

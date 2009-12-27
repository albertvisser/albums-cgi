#! C:/python23 python
# -*- coding: UTF-8 -*-

import muziek_globals
htmlpad = muziek_globals.htmlpad
cssfile = muziek_globals.cssfile
cgipad = muziek_globals.cgipad
from muziek_artiest import ArtiestenLijst
from muziek_artiest import Artiest

class Fout(Exception):
    pass

class artiesten_main:
    def __init__(self,args):
        if args.has_key("editEntry"):
            self.editEntry = args["editEntry"]
        else:
            raise Fout("Geen edit-mode (editEntry) opgegegeven")
            return
        if args.has_key("selId"):
            self.selId = args["selId"]
        else:
            self.selId = '0'
        if args.has_key("afterId"):
            self.afterId = args["afterId"]
        else:
            self.afterId = '0'
        if args.has_key("sSort"):
            self.sSort = args["sSort"]
        else:
            self.sSort = ''
        lh = ArtiestenLijst()
        self.regels = []
        herhaal = False
        for x in file(htmlpad + "artiesten.html"):
            if herhaal:
                self.herh_regels.append(x[:-1])
                if x[:-1].strip() == "</tr>":
                    herhaal = False
                    for y in lh.Namen:
                        if not self.editEntry:
                            if y[0] == self.selId:
                                self.editEntry = True
                            else:
                                self.maakregel(y)
                                if y[0] == self.afterId:
                                    self.editEntry = True
                        if self.editEntry:
                            self.editEntry = False
                            self.maakregel(y)
            elif x[:-1].strip() == "<tr>":
                herhaal = True
                self.herh_regels = [x[:-1]]
            elif "stylesheet" in x:
                self.regels.append(x[:-1] % cssfile)
            elif "hNieuw" in x:
                self.regels.append(x[:-1] % cgipad)
            else:
                self.regels.append(x[:-1])

    def maakregel(self,x):
        self.regels.append(self.herh_regels[0])
        if self.editEntry:
            self.regels.append(self.herh_regels[1] % cgipad)
        h1 = self.herh_regels[2].split("$s")
        h2 = self.herh_regels[3].split("$s")
        if self.editEntry:
            if self.selId == 0:
                self.regels.append("".join(h1) % (x[0],""))
                self.regels.append("".join(h2) % (x[0],self.sSort))
            elif x[0] == selid:
                self.regels.append("".join(h1) % (x[0],('value="%s"' % x[1])))
                self.regels.append("".join(h2) % (x[0],x[2]))
        else:
            self.regels.append("%s%s%s" % (h1[0],x[1],h1[2]))
            self.regels.append("%s%s%s" % (h2[0],x[2],h2[2]))
        self.regels.append(self.herh_regels[4])
        if self.editEntry:
            self.regels.append(self.herh_regels[5] % x[0])
        else:
            self.regels.append(self.herh_regels[6] % (cgipad,x[0]))
        if self.editEntry:
            self.regels.append(self.herh_regels[7])
            self.regels.append(self.herh_regels[8])
        else:
            self.regels.append(self.herh_regels[9] % (cgipad,x[0],x[2]))
        self.regels.append(self.herh_regels[10])
        if self.editEntry:
            self.regels.append(self.herh_regels[11])
        self.regels.append(self.herh_regels[12])

class artiest_wijzig:
    def __init__(self,args):
        if args.has_key("selId"):
            self.selId = args["selId"]
        else:
            raise Fout("Geen selId opgegegeven")
            return
        if args.has_key("hNaam"):
            self.hNaam = args["hNaam"]
        else:
            raise Fout("Geen hNaam opgegegeven")
            return
        if args.has_key("hSort"):
            self.hSort = args["hSort"]
        else:
            raise Fout("Geen hSort opgegegeven")
            return

        if self.selId == "0":
            ln = Artiest(0)
            self.selId = ln.Id
        ih = Artiest(self.selId)
        #~ s.append("<br />vóór lezen:")
        #~ s.append('<br />Id: %s' % ih.Id )
        #~ s.append('<br />Naam: %s' % ih.Naam )
        #~ s.append('<br />Sort: %s' % ih.sort )
        hwijzig = False
        ih.read()
        if ih.found:
            #~ s.append("<br /><br />vóór wijzigen:")
            #~ s.append('<br />Id: %s' % ih.Id )
            #~ s.append('<br />Naam: %s' % ih.Naam )
            #~ s.append('<br />Sort: %s' % ih.sort )
            if self.hNaam != ih.Naam :
                ih.wijzigNaam(self.hNaam)
                hwijzig = True
            if self.hSort != ih.Sort :
                ih.wijzigSort(self.hSort)
                hwijzig = True
            #~ s.append('<br /><br />na wijzigen:')
            #~ s.append('<br />Id: %s' % ih.Id )
            #~ s.append('<br />Naam: %s' % ih.Naam )
            #~ s.append('<br />Sort: %s' % ih.sort )
        else:
            ih.wijzigNaam(self.hNaam)
            ih.wijzigSort(self.hSort)
            hwijzig = True
        if hwijzig:
            ih.write()

def test(num):
    if num == 1:
        args = {"editEntry": False}
    elif num == 2: # form.has_key("hNieuw"):
        args = {"editEntry": True}
    elif num == 3: # form.has_key("edit"):
        args = {"editEntry": True}
        args["selId"] = form["edit"].value
    elif num == 4: # form.has_key("after"):
        args = {"editEntry": True}
        args["afterId"] = form["after"].value
        args["sSort"] = form["sort"].value
    elif num == 11:
        args = {}
        args["selId"] = form["hId"].value
        args["hNaam"] = form["tnaam"].value
        args["hSort"] = form["tsort"].value
        try:
            m = artiest_wijzig(args)
        except Fout,meld:
            print meld
            return
        args = {"editEntry": False}
    try:
        m = artiesten_main(args)
    except Fout,meld:
        print meld
    else:
        f = open(("test_%s.html" % str(num)),"w")
        for x in m.regels:
            f.write("%s\n" % x)
        f.close()

if __name__ == "__main__":
    test(1)
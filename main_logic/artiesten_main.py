# -*- coding: UTF-8 -*-
import os
import globals
from artiest import artiestenlijst, Artiest

class Fout(Exception):
    pass

class Artiesten(object):
    def __init__(self, args):
        ## self.regels = [str(args)]
        ## return
        edit = args.get("editEntry", None)
        self.sel_id = args.get("selId", '0')
        self.after_id = args.get("afterId", '0')
        self.sortval = args.get("sSort", '')
        if edit is None:
            raise Fout("Geen edit-mode (editEntry) opgegegeven")
            return
        self.regels = []
        herhaal = False
        with open(os.path.join(globals.htmlpad, "artiesten.html")) as _in:
            for x in _in:
                x = x.rstrip()
                if x == '<!-- kop -->':
                    self.regels.extend(globals.kop('artiest'))
                elif herhaal:
                    self.herh_regels.append(x)
                    if x.lstrip() == "</tr>":
                        herhaal = False
                        if edit and self.sel_id == '0':
                            self.maakregel('0', edit=True)
                            self.edit = False
                        for y in artiestenlijst():
                            if edit:
                                if y[0] == self.sel_id:
                                    self.maakregel(y, edit=True)
                                else:
                                    self.maakregel(y)
                                    if y[0] == self.after_id:
                                        self.maakregel('0', edit=True)
                            else:
                                self.maakregel(y)
                elif x.lstrip() == "<tr>":
                    herhaal = True
                    self.herh_regels = [x]
                elif "stylesheet" in x:
                    self.regels.append(x % globals.cssfile)
                elif "hNieuw" in x:
                    self.regels.append(x % globals.cgipad)
                else:
                    self.regels.append(x)

    def maakregel(self, x, edit=False):
        if x == '0':
            x = ('0', '', self.sortval)
        self.regels.append(self.herh_regels[0])
        if edit:
            self.regels.append(self.herh_regels[1] % globals.cgipad)
        h1 = self.herh_regels[2].split("$s")
        h2 = self.herh_regels[3].split("$s")
        if edit:
            self.regels.append("".join(h1) % (x[0], 'value="{}"'.format(x[1])))
            self.regels.append("".join(h2) % (x[0], x[2]))
        else:
            self.regels.append("".join((h1[0], x[1], h1[2])))
            self.regels.append("".join((h2[0], x[2], h2[2])))
        self.regels.append(self.herh_regels[4])
        if edit:
            self.regels.append(self.herh_regels[5] % x[0])
        else:
            self.regels.append(self.herh_regels[6] % (globals.cgipad, x[0]))
        if edit:
            self.regels.append(self.herh_regels[7])
            self.regels.append(self.herh_regels[8])
        else:
            self.regels.append(self.herh_regels[9] % (globals.cgipad, x[0], x[2]))
        self.regels.append(self.herh_regels[10])
        if edit:
            self.regels.append(self.herh_regels[11])
        self.regels.append(self.herh_regels[12])

def wijzig_artiest(args):
    wijzig = False
    sel_id = args.get("selId", None)
    if sel_id is None:
        raise Fout("Geen selId opgegegeven")
    naam = args.get("hNaam", None)
    if naam is None:
        raise Fout("Geen hNaam opgegegeven")
    sort = args.get("hSort", None)
    if sort is None:
        raise Fout("Geen hSort opgegegeven")
    if sel_id == "0":
        sel_id = Artiest(0).id
    ih = Artiest(sel_id)
    ih.read()
    if ih.found:
        if ih.naam != naam:
            ih.naam = naam
            wijzig = True
        if ih.sort != sort:
            ih.sort = sort
            wijzig = True
    else:
        ih.naam = naam
        ih.sort = sort
        wijzig = True
    if wijzig:
        ih.write()

if __name__ == "__main__":
    test(1)

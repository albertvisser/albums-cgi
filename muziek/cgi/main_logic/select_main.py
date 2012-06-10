import globals
from studio import albumlist
from live import concertlist
from artiest import Artiest, artiestenlijst
startform = """\
  <div class="wide"><span>
     <form action="http://muziek.pythoneer.nl/cgi-bin/muziek_select.py" method="post">
      Snel naar dezelfde selectie voor een andere artiest:
      <select name="selArtiest" id="selArtiest" onchange="form.submit()">
       <option value="0">-- selecteer --</option>
"""
optiontext = '    <option value="%s">%s</option>'
endselect = '      </select>'
hidden_inputs = """\
      <input type="hidden" name="hType" value="%s" />
      <input type="hidden" name="hZoek" value="%s" />
      <input type="hidden" name="hSort" value="%s" />
"""
endform = '     </form></span></div>'

class Select(object):
    def __init__(self):
        # opname (niet 1 op 1) laten we even liggen
        #~ if sorteren == 'opname' or sZoek == 'opname':
            #~ list.append('opname')
        self.regels = []
        self.selection = {}
        self.fieldslist = ''
        self.itemlist = []
        self.fout = ''

    def set_arg(self, name, value):
        ok = True
        if name == 'sZoek':
            self.selecteren = value
        elif name == 'tZoek':
            self.zoektekst = value
        elif name == 'albumtype':
            self.albumtype = value
        elif name == 'sorteren':
            self.sorteren = value
        else:
            ok = False
        return ok

    def go(self):
        if self.init_sel():
            if self.albumtype == "studio":
                self.sorteer_studio()
            elif self.albumtype == "live":
                self.sorteer_live()
            self.maakregels()
        else:
            self.regels.append('Location: %smuziek_start.py?fout=%s' % (
                globals.cgipad, self.fout))
            self.regels.append('')

    def init_sel(self):
        if self.albumtype == "studio":
            self.fieldslist = ['artiest', 'titel']
        elif self.albumtype == "live":
            self.fieldslist = ['artiest', 'locatie', 'datum']
        else:
            self.fout = 'Geen albumtype kunnen bepalen'
            return False
        try:
            self.selecteren
        except AttributeError:
            self.selecteren = ""
        try:
            self.zoektekst
        except AttributeError:
            self.zoektekst = ""
        if self.selecteren == "artiest":
            self.selection[self.selecteren] = self.zoektekst
            ah = Artiest(self.zoektekst, '1')
            self.onthouden_zoektekst = self.zoektekst
            self.zoektekst = ah.naam
        else:
            self.selection[self.selecteren] = self.zoektekst
        if self.sorteren == 'jaar':
            self.fieldslist.append('jaar')
            self.fieldslist.append('volgnr')

        if self.albumtype == "studio":
            if len(self.selection) > 0:
                self.itemlist = albumlist(self.fieldslist, self.selection)
            else:
                self.itemlist = albumlist(self.fieldslist)
        if self.albumtype == "live":
            if len(self.selection) > 0:
                self.itemlist = concertlist(self.fieldslist, self.selection)
            else:
                self.itemlist = concertlist(self.fieldslist)
        if len(self.itemlist) == 0:
            f = ''
            if len(self.selection) > 0:
                if self.selecteren == "artiest":
                    f = 'bij {}  "{}"'.format(self.selecteren, self.zoektekst)
                else:
                    f = 'met "{}" in "{}"'.format(self.zoektekst, self.selecteren)
            self.fout = 'Geen {} albums gevonden {}'.format(self.albumtype, f)
            return False
        return True

    def sorteer_studio(self):
        h = '  Lijst studio-albums'
        if self.selecteren == '':
            h += ': geen selectie'
        else:
            h += ': selectie op %s "%s"' % (self.selecteren, self.zoektekst)
        if self.sorteren == "":
            h += "; geen sortering"
            ## for x in self.itemlist:
                ## y = [x[0], x[1], x[2]]
                ## self.sl.append(y)
        else:
            h += '; sortering op %s' % self.sorteren
            sortlist = []
            if self.sorteren == 'titel':
                ## sortlist = [";#;".join(x) for x in self.itemlist]
                for x in self.itemlist:
                    y = x[2] + ";#;" + x[1] + ";#;" + x[0]
                    sortlist.append(y)
                sortlist.sort() ## was self.sortlist
                self.itemlist = [] # reversed(x.split(';#;')) for x in sortlist]
                for x in sortlist:
                    y = x.split(";#;")
                    z = [y[2],y[1],y[0]]
                    self.itemlist.append(z)
            elif self.sorteren == 'jaar':
                for x in self.itemlist:
                    y = x[3] + x[4] + ";#;" + x[2] + ";#;" + x[1] + ";#;" + x[0]
                    sortlist.append(y)
                sortlist.sort()
                self.itemlist = [] # reversed(x.split(";#;")[1:]) for x in sortlist]
                for x in sortlist:
                    y = x.split(";#;")
                    z = [y[3], y[2], y[1]]
                    self.itemlist.append(z)
            elif self.sorteren == 'artiest':
                # via de aparte sorteersleutel
                for x in self.itemlist:
                    ah = Artiest(x[1].decode('ISO-8859-1'), '0')
                    y = ah.sort + ";#;" + x[2] + ";#;" + x[1] + ";#;" + x[0]
                    sortlist.append(y)
                sortlist.sort()
                self.itemlist = [] # reversed(x.split(';#;')[1:]) for x in sortlist]
                for x in sortlist:
                    y = x.split(";#;")
                    z = [y[3], y[2], y[1]]
                    self.itemlist.append(z)
        self.titel = h

    def sorteer_live(self):
        h = '  Lijst concert-opnames'
        if self.selecteren == '':
            h += ': geen selectie'
        else:
            h += ': selectie op %s "%s"' % (self.selecteren, self.zoektekst)
        if self.sorteren == "":
            h += "; geen sortering"
            ## for x in self.fl.Items:
                ## y = [x[0], x[1], x[2], x[3]]
                ## self.sl.append(y)
        else:
            h = h + ('; sortering op %s' % self.sorteren)
            sortlist = []
            if self.sorteren == "plaats":
                ## sortlist = [";#;".join((x[2], x[3], x[1], x[0]))
                    ## for x in self.itemlist]
                for x in self.itemlist:
                    y = x[2] + ";#;" + x[3] + ";#;" + x[1] + ";#;" + x[0]
                    sortlist.append(y)
                sortlist.sort()
                self.itemlist = []
                for x in sortlist:
                    y = x.split(";#;")
                    z = [y[4], y[3], y[1], y[2]]
                    self.itemlist.append(z)
            elif self.sorteren == "datum":
                for x in self.itemlist:
                    y = x[3] + ";#;" + x[1] + ";#;" + x[2] + ";#;" + x[0]
                    sortlist.append(y)
                sortlist.sort()
                self.itemlist = []
                for x in sortlist:
                    y = x.split(";#;")
                    z = [y[3], y[1], y[2], y[0]]
                    self.itemlist.append(z)
            elif self.sorteren == 'artiest':
                # via de aparte sorteersleutel
                for x in self.itemlist:
                    ah = Artiest(x[1].decode('ISO-8859-1'), '0')
                    y = ah.sort + ";#;" + x[2] + ";#;" + x[3] + ";#;" + x[1] + ";#;" + x[0]
                    sortlist.append(y)
                sortlist.sort()
                self.itemlist = []
                for x in sortlist:
                    y = x.split(";#;")
                    z = [y[4], y[3], y[1], y[2]]
                    self.itemlist.append(z)
        self.titel = h

    def maakregels(self):
        with open("%sselect.html" % globals.htmlpad) as fh:
            in_form = False
            for x in fh:
                x = x.rstrip()
                if in_form:
                    if x.startswith("<!--"):
                        continue
                    formregels.append(x)
                    if "</form" in x:
                        in_form = False
                        for y in self.itemlist: # y[0] is de sleutelwaarde
                            if self.albumtype == "studio":
                                if self.sorteren == 'opname' and self.selecteren == 'opname':  #        lh.Items bestaat uit id, artiest, titel en loc
                                    h = ('%s: %s - %s' % (y[3],y[1],y[2]))
                                else:
                                    if self.selecteren == 'opname':                       #        lh.Items bestaat uit id, artiest, titel en loc
                                        h = ('%s - %s (%s)' % (y[1],y[2],y[3]))
                                    else:                                        #        fl.Items bestaat uit id, artiest en titel
                                        h =('%s - %s' % (y[1],y[2]))
                            if self.albumtype == "live":
                                if self.sorteren == 'opname' and self.selecteren == 'opname':  #        lh.Items bestaat uit id, artiest, titel en loc
                                    h = ('%s: %s - %s, %s' % (y[4],y[1],y[2],y[3]))
                                else:
                                    if self.selecteren == 'opname':                      #        lh.Items bestaat uit id, artiest, titel en loc
                                        h = ('%s - %s, %s (%s)' % (y[1],y[2],y[3],y[4]))
                                    else:                                       #        fl.Items bestaat uit id, artiest en titel
                                        h = ('%s - %s, %s' % (y[1],y[2],y[3]))
                            self.regels.append(formregels[0] % globals.cgipad)
                            self.regels.append(formregels[1] % h)
                            self.regels.append(formregels[2] % y[0])
                            self.regels.append(formregels[3] % self.albumtype)
                            self.regels.append(formregels[4] % self.selecteren)
                            if self.selecteren == "artiest":
                                self.regels.append(formregels[5] % self.onthouden_zoektekst)
                            else:
                                self.regels.append(formregels[5] % self.zoektekst)
                            self.regels.append(formregels[6] % self.sorteren)
                            self.regels.append(formregels[7])
                            self.regels.append(formregels[8])
                elif "<form" in x:
                    formregels = [x]
                    in_form = True
                elif x == "<!-- kop -->":
                    for x in globals.kop("select"):
                        self.regels.append(x)
                elif x == "<!-- selectie -->":
                    if self.albumtype == "studio":
                        h = '  Lijst studio-albums'
                    if self.albumtype == 'live':
                        h = '  Lijst concert-opnames'
                    if self.selecteren == '':
                        h = h + ': geen selectie'
                    else:
                        if self.selecteren == "artiest":
                            h += ': selectie op %s "%s"' % (self.selecteren,
                                self.zoektekst)
                        else:
                            h += ': selectie op %s: "%s"' % (self.selecteren,
                                self.selection[self.selecteren])
                    if self.sorteren == 'geen':
                        h += "; geen sortering"
                    else:
                        h += '; sortering op %s' % self.sorteren
                    self.regels.append(h)
                elif x == "<!-- selArtiest -->" and self.selecteren == 'artiest':
                    self.regels.append(startform)
                    for y in artiestenlijst():
                        self.regels.append(optiontext % (y[0],y[1]))
                    self.regels.append(endselect)
                    self.regels.append(hidden_inputs % (self.albumtype,
                        self.selecteren, self.sorteren))
                    self.regels.append(endform)
                elif "hType" in x:
                    self.regels.append(x % self.albumtype)
                elif "hZoek" in x:
                    self.regels.append(x % self.selecteren)
                elif "hSort" in x:
                    self.regels.append(x % self.sorteren)
                else:
                    self.regels.append(x)
            self.regels.insert(0, '')

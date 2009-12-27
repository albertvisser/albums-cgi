import muziek_globals
htmlpad = muziek_globals.htmlpad
cgipad = muziek_globals.cgipad
from muziek_studio_met import AlbumList
from muziek_live_met import ConcertList
from muziek_artiest import Artiest
from muziek_artiest import ArtiestenLijst

class select_main:
    def __init__(self):
        # opname (niet 1 op 1) laten we even liggen
        #~ if sorteren == 'opname' or sZoek == 'opname':
            #~ list.append('opname')
        self.regels = []
        self.selection = {}
        self.list = ''
        self.sortList = []
        self.sl = []

    def setArg(self,name,value):
        ok = True
        if name == 'sZoek':
            self.sZoek = value
        elif name == 'tZoek':
            self.tZoek = value
        elif name == 'albumtype':
            self.albumtype = value
        elif name == 'sorteren':
            self.sorteren = value
        else:
            ok = False
        return ok

    def go(self):
        if self.initSel():
            if self.albumtype == "studio":
                self.sorteerStudio()
            elif self.albumtype == "live":
                self.sorteerLive()
            self.maakregels()

    def initSel(self):
        if self.albumtype == "studio":
            self.list = ['artiest','titel']
        elif self.albumtype == "live":
            self.list = ['artiest','locatie','datum']
        else:
            self.regels.append('Location: %sMuziek_Start.py?fout=Geen albumtype kunnen bepalen' % cgipad)
            self.regels.append('')
            return False

        if self.sZoek == "artiest":
            self.selection[self.sZoek] = self.tZoek
            ah = Artiest(self.tZoek,'1')
            self.tZoekN = self.tZoek
            self.tZoek = ah.Naam
        else:
            self.selection[self.sZoek] = self.tZoek
        if self.sorteren == 'jaar':
            self.list.append('jaar')
            self.list.append('volgnr')

        if self.albumtype == "studio":
            if len(self.selection) > 0:
                self.fl = AlbumList(self.list, self.selection)
            else:
                self.fl = AlbumList(self.list)
        if self.albumtype == "live":
            if len(self.selection) > 0:
                self.fl = ConcertList(self.list, self.selection)
            else:
                self.fl = ConcertList(self.list)
        if len(self.fl.Items) == 0:
            f = ''
            if len(self.selection) > 0:
                if self.sZoek == "artiest":
                    f = (' bij %s  "%s"' % (self.sZoek, self.tZoek))
                else:
                    f = (' met "%s" in "%s"' % (self.tZoek, self.sZoek))
            self.regels.append('Location: %sMuziek_Start.py?fout=Geen %s albums gevonden%s' % (cgipad,self.albumtype,f))
            self.regels.append('')
            return False
        return True

    def sorteren(self):
    #-- de list sorteren
        #~ if self.sorteren == 'opname': #- voorlopig niet mogelijk
            #~ for x in fl.Items:
                #~ if x[1] != None:
                    #~ y = x[1] + ";#; " + x[2] + ";#;" + x[0]
                    #~ self.sortList.append(y)
            #~ self.sortList.sort()
            #~ for x in self.sortList:
                #~ y = x.split(";#;")
                #~ self.sl.append(y)
        h = "..."

    def sorteerStudio(self):
        h = '  Lijst studio-albums'
        if self.sZoek == '':
            h = h + ': geen selectie'
        else:
            h = h + (': selectie op %s "%s"' % (self.sZoek, self.tZoek))
        if self.sorteren == 'titel':
            h = h + ('; sortering op %s' % self.sorteren)
            for x in self.fl.Items:
                y = x[2] + ";#;" + x[1] + ";#;" + x[0]
                self.sortList.append(y)
            self.sortList.sort()
            for x in self.sortList:
                y = x.split(";#;")
                z = [y[2],y[1],y[0]]
                self.sl.append(z)
        elif self.sorteren == 'jaar':
            h = h + ('; sortering op %s' % self.sorteren)
            for x in self.fl.Items:
                y = x[3] + x[4] + ";#;" + x[2] + ";#;" + x[1] + ";#;" + x[0]
                self.sortList.append(y)
            self.sortList.sort()
            for x in self.sortList:
                y = x.split(";#;")
                z = [y[3],y[2],y[1]]
                self.sl.append(z)
        elif self.sorteren == 'artiest':
            h = h + ('; sortering op %s' % self.sorteren)
            # via de aparte sorteersleutel
            for x in self.fl.Items:
                ah = Artiest(x[1].decode('ISO-8859-1'), '0')
                y = ah.sort + ";#;" + x[2] + ";#;" + x[1] + ";#;" + x[0]
                self.sortList.append(y)
            self.sortList.sort()
            for x in self.sortList:
                y = x.split(";#;")
                z = [y[3],y[2],y[1]]
                self.sl.append(z)
        else:
            h = h + "; geen sortering"
            for x in self.fl.Items:
                y = [x[0], x[1], x[2]]
                self.sl.append(y)
        self.titel = h

    def sorteerLive(self):
        h = '  Lijst concert-opnames'
        if self.sZoek == '':
            h = h + ': geen selectie'
        else:
            h = h + (': selectie op %s "%s"' % (self.sZoek, self.tZoek))
        if self.sorteren == "plaats":
            h = h + ('; sortering op %s' % self.sorteren)
            for x in self.fl.Items:
                y = x[2] + ";#;" + x[3] + ";#;" + x[1] + ";#;" + x[0]
                self.sortList.append(y)
            self.sortList.sort()
            for x in self.sortList:
                y = x.split(";#;")
                z = [y[4],y[3],y[1],y[2]]
                self.sl.append(z)
        elif self.sorteren == "datum":
            h = h + ('; sortering op %s' % self.sorteren)
            for x in self.fl.Items:
                y = x[3] + ";#;" + x[1] + ";#;" + x[2] + ";#;" + x[0]
                self.sortList.append(y)
            self.sortList.sort()
            for x in self.sortList:
                y = x.split(";#;")
                z = [y[3],y[1],y[2],y[0]]
                self.sl.append(z)
        elif self.sorteren == 'artiest':
            h = h + ('; sortering op %s' % self.sorteren)
            # via de aparte sorteersleutel
            for x in self.fl.Items:
                ah = Artiest(x[1].decode('ISO-8859-1'), '0')
                y = ah.sort + ";#;" + x[2] + ";#;" + x[3] + ";#;" + x[1] + ";#;" + x[0]
                self.sortList.append(y)
            self.sortList.sort()
            for x in self.sortList:
                y = x.split(";#;")
                z = [y[4],y[3],y[1],y[2]]
                self.sl.append(z)
        else:
            h = h + "; geen sortering"
            for x in self.fl.Items:
                y = [x[0], x[1], x[2], x[3]]
                self.sl.append(y)
        self.titel = h

    def maakregels(self):
        fh = open("%sselect.html" % htmlpad)
        inForm = False
        for x in fh.readlines():
            if inForm:
                if x[:4] == "<!--": continue
                formregels.append(x[:-1])
                if x.find("</form") >= 0:
                    inForm = False
                    for y in self.sl: # y[0] is de sleutelwaarde
                        if self.albumtype == "studio":
                            if self.sorteren == 'opname' and self.sZoek == 'opname':  #        lh.Items bestaat uit id, artiest, titel en loc
                                h = ('%s: %s - %s' % (y[3],y[1],y[2]))
                            else:
                                if self.sZoek == 'opname':                       #        lh.Items bestaat uit id, artiest, titel en loc
                                    h = ('%s - %s (%s)' % (y[1],y[2],y[3]))
                                else:                                        #        fl.Items bestaat uit id, artiest en titel
                                    h =('%s - %s' % (y[1],y[2]))
                        if self.albumtype == "live":
                            if self.sorteren == 'opname' and self.sZoek == 'opname':  #        lh.Items bestaat uit id, artiest, titel en loc
                                h = ('%s: %s - %s, %s' % (y[4],y[1],y[2],y[3]))
                            else:
                                if self.sZoek == 'opname':                      #        lh.Items bestaat uit id, artiest, titel en loc
                                    h = ('%s - %s, %s (%s)' % (y[1],y[2],y[3],y[4]))
                                else:                                       #        fl.Items bestaat uit id, artiest en titel
                                    h = ('%s - %s, %s' % (y[1],y[2],y[3]))
                        self.regels.append(formregels[0] % cgipad)
                        self.regels.append(formregels[1] % h)
                        self.regels.append(formregels[2] % y[0])
                        self.regels.append(formregels[3] % self.albumtype)
                        self.regels.append(formregels[4] % self.sZoek)
                        if self.sZoek == "artiest":
                            self.regels.append(formregels[5] % self.tZoekN)
                        else:
                            self.regels.append(formregels[5] % self.tZoek)
                        self.regels.append(formregels[6] % self.sorteren)
                        self.regels.append(formregels[7])
                        self.regels.append(formregels[8])
            elif x.find("<form") >= 0:
                formregels = [x[:-1]]
                inForm = True
            elif x[:-1] == "<!-- kop -->":
                h = muziek_globals.kop("select")
                for x in h.regels:
                    self.regels.append(x)
            elif x[:-1] == "<!-- selectie -->":
                if self.albumtype == "studio":
                    h = '  Lijst studio-albums'
                if self.albumtype == 'live':
                    h = '  Lijst concert-opnames'
                if self.sZoek == '':
                    h = h + ': geen selectie'
                else:
                    if self.sZoek == "artiest":
                        h = h + (': selectie op %s "%s"' % (self.sZoek, self.tZoek))
                    else:
                        h = h + (': selectie op %s: "%s"' % (self.sZoek, self.selection[self.sZoek]))
                if self.sorteren == 'geen':
                    h = h + "; geen sortering"
                else:
                    h = h + ('; sortering op %s' % self.sorteren)
                self.regels.append(h)
            elif x[:-1] == "<!-- selArtiest -->":
                self.regels.append('  <div class="wide"><span>')
                self.regels.append('     <form action="http://muziek.pythoneer.nl/cgi-bin/muziek_select.py" method="post">')
                self.regels.append('      Snel naar dezelfde selectie voor een andere artiest:')
                self.regels.append('      <select name="selArtiest" id="selArtiest" onchange="form.submit()">')
                self.regels.append('       <option value="0">-- selecteer --</option>')
                al = ArtiestenLijst()
                for y in al.Namen:
                    self.regels.append('    <option value="%s">%s</option>' % (y[0],y[1]))
                self.regels.append('      </select>')
                self.regels.append('      <input type="hidden" name="hType" value="%s" />' % self.albumtype)
                self.regels.append('      <input type="hidden" name="hZoek" value="%s" />' % self.sZoek)
                self.regels.append('      <input type="hidden" name="hSort" value="%s" />' % self.sorteren)
                self.regels.append('     </form></span></div>')
            elif x.find("hType") >= 0:
                self.regels.append(x[:-1] % self.albumtype)
            elif x.find("hZoek") >= 0:
                self.regels.append(x[:-1] % self.sZoek)
            elif x.find("hSort") >= 0:
                self.regels.append(x[:-1] % self.sorteren)
            else:
                self.regels.append(x[:-1])
        fh.close()
        self.regels.insert(0,'')

if __name__ == '__main__':
    h = select_main()
    h.setArg('albumtype',"studio")
    h.setArg('sZoek',"artiest")
    h.setArg('tZoek',"6") # the Allman Brothers Band
    h.setArg('sorteren',"geen")
    h.go()
    for x in h.regels:
        print x

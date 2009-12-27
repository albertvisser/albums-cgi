import string
from muziek_globals import *
from muziek_artiest import Artiest
from muziek_studio_met import Album
from muziek_live_met import Concert
from muziek_studio_met import AlbumList
from muziek_live_met import ConcertList

class detail_main:
    def __init__(self,typ,wijzigO,id=""):
        self.regels = []
        if typ == 'studio' or typ == 'live':
            self.albumtype = typ
        else:
            self.meldfout("Geen albumtype opgegeven")
            return
        self.setAttr("wijzigO",wijzigO)
        self.setAttr("albumid",id)
        self.setAttr("nieuw",False)
        self.setAttr("artiest","")
        self.setAttr("titel","")
        if self.albumtype == 'studio':
            self.setAttr("label","")
            self.setAttr("jaar","")
            self.setAttr("volgnr","")
            self.setAttr("producer","")
            self.setAttr("credits","")
        elif self.albumtype == 'live':
            self.setAttr("locatie","")
            self.setAttr("datum","")
        self.setAttr("bezetting","")
        self.tracks = []
        self.opnames = []

    def setAttr(self,x,y):
        if x == "albumid":
            if y != 0:
                self.Id = y
            elif self.albumtype == 'studio':
                dh = Album(0)
                self.Id = dh.id
            elif self.albumtype == 'live':
                dh = Concert(0)
                self.Id = dh.id
        elif x == "sZoek":
            self.sZoek = y
        elif x == "tZoek":
            self.tZoek = y
        elif x == "Sort":
            self.Sort = y
        elif x == "wijzigO":
            self.wijzigO = y
        elif x == "nieuw":
            self.nieuwAlbum = y
        elif x == "artiest":
            self.Artiest = y
        elif x == "titel":
            self.Titel = y
        elif x == "label":
            self.Label = y
        elif x == "jaar":
            self.Jaar = y
        elif x == "producer":
            self.Produced = y
        elif x == "credits":
            self.Credits = y
        elif x == "bezetting":
            self.Bezetting = y
        elif x == "locatie":
            self.locatie = y
        elif x == "datum":
            self.datum = y
        elif x == "volgnr":
            self.volgnr = y
        elif x == "tracks":
            self.Tracks = y
        elif x == "opnames":
            self.Opnames = y
        elif x == "tracks":
            for z in y.split("\n"):
                self.tracks.append(z)
        elif x == "opnames":
            for z in y.split("\n"):
                self.opnames.append(z)

    def wijzig(self):
        self.ok = True
        if self.Artiest == "":
            self.meldfout("wijzigen niet mogelijk, artiestnaam onbekend")
            return
        if self.Titel != "":
            self.meldfout("wijzigen niet mogelijk, titel onbekend")
            return
        if self.Type == 'studio':
            dh = Album(self.Id)
        elif self.Type == 'live':
            dh = Concert(self.Id)
        dh.read()
        dh.wijzigArtiest(self.Artiest)
        dh.wijzigTitel(self.Titel.replace("&","&amp;"))
        if self.Label != "":
            dh.wijzigLabel(self.Label.replace("&","&amp;"))
        if self.Jaar != "":
            dh.wijzigJaar(self.Jaar)
        if self.Produced != "":
            dh.wijzigProducer(self.Produced.replace("&","&amp;"))
        if self.Credits != "":
            dh.wijzigCredits(self.Credits.replace("&","&amp;"))
        if self.Bezetting != "":
            dh.wijzigBezetting(self.Bezetting.replace("&","&amp;"))
        if self.Tracks != "":
            trks = self.Tracks.split("\n")
            for y in dh.Tracks:
                dh.remTrack(y)
            for y in trks:
                if y[-1] == "\n":
                    y = y[:-1]
                dh.addTrack(y.replace("&","&amp;"))
        if self.Opnames != "":
            opn = self.Opnames.split("\n")
            # hier is het ingewikkelder omdat het eerste deel van de tekst
            # bestaat uit een waarde die eigenlijk uit een selectielijst moet komen
        dh.write()

    def toon(self):
        if self.albumtype == 'studio':
            ih = Album(self.Id)
        elif self.albumtype == 'live':
            ih = Concert(self.Id)
        else:
            self.meldfout("Geen albumtype opgegeven")
            return
        ih.read()
        if not ih.found:
            self.meldfout("Album-gegevens niet aanwezig")
            return
        artiest = ih.Artiest
        dh = Artiest(ih.Artiest, '0')
        if self.albumtype == 'studio':
            titel = ih.Titel
            label = ih.Label
            jaar = ih.Jaar
            volgnr = ih.Volgnr
            producer = ih.Producer
            credits = ih.Credits
            lh = AlbumList(['artiest','titel'],{"artiest": dh.Id})
        if self.albumtype == 'live':
            locatie = ih.Locatie
            datum = ih.Datum
            lh = ConcertList(['artiest','locatie','datum'],{"artiest": dh.Id})
        bezetting = ih.Bezetting
        tracks = ih.Tracks
        opnames = ih.Opnames

        if self.albumtype == 'studio': fh = open(htmlpad + "detail.html")
        if self.albumtype == 'live': fh = open(htmlpad + "detail_live.html")
        spc = ' '
        tracknr = 1
        opnamenr = 1
        TrackListLines = False
        OpnListLines = False
        inProd = False
        inCred = False
        inBezet = False
        from muziek_artiest import ArtiestenLijst
        al = ArtiestenLijst()
        for x in fh.readlines():
            xh = x[:-1].split()
            if xh[0] == "<!--":
                if len(xh) == 1: continue
                if xh[1] == "kop":
                    h = kop("detail",self.albumtype,self.sZoek,self.tZoek,self.Sort)
                    for x in h.regels:
                        self.regels.append(x)
                elif xh[1] == "artiest":
                    # <!-- artiest   <input type="text" name="txtArtiest" id="txtArtiest" size="20" maxlength="60" value="%s"/><br /> -->
                    self.regels.append('    <select name="selArtiest" id="selArtiest">')
                    for y in al.Namen:
                        if y[1] == artiest.encode("ISO-8859-1"):
                            self.regels.append('    <option selected value="%s">%s</option>' % (y[0],y[1]))
                        else:
                            self.regels.append('    <option value="%s">%s</option>' % (y[0],y[1]))
                    self.regels.append("    </select>")
                elif xh[1] == "titel":
                    #~ <!-- titel     <input type="text" name="txtTitel" id="txtTitel" size="60" maxlength="80" value="%s" /> -->
                    s = spc.join(xh[2:-1])
                    if self.nieuwAlbum:
                        self.regels.append(s.replace("%s",""))
                    else:
                        self.regels.append(s.replace("%s",titel))
                elif xh[1] == "id":
                    # <!-- id hIdAlbum <input type="hidden" name="hWijzig" id="hWijzig" value="%s" /> -->
                    s = xh[3:]
                    ss = s[:-1]
                    ss[2] = 'name="' + xh[2] + '"'
                    ss[3] = 'id="' + xh[2] + '"'
                    ss[4] = 'value="' + self.Id + '"'
                    self.regels.append('   %s' % spc.join(ss))
                elif xh[1] == "type":
                    # <!-- type hTypeAlbum <input type="hidden" name="hWijzig" id="hWijzig" value="%s" /> -->
                    s = xh[3:]
                    ss = s[:-1]
                    ss[2] = 'name="' + xh[2] + '"'
                    ss[3] = 'id="' + xh[2] + '"'
                    ss[4] = 'value="' + self.albumtype + '"'
                    self.regels.append('   %s' % spc.join(ss))
                elif xh[1] == "update":
                    # <!-- update      <input type="submit" abled value="Tracks aanpassen" /> -->
                    s = xh[2:]
                    ss = s[:-1]
                    ss[2] = ""
                    if self.nieuwAlbum:
                        ss[2] = 'disabled="disabled"'
                    self.regels.append('   %s' % spc.join(ss))
                elif x[5:10] == "label":
                    # <!-- label     <input type="text" name="txtLabel" id="txtLabel" size="20" maxlength="80" value="%s"/><br /> -->
                    p = x[11:]
                    p = p[:-4]
                    if label != "":
                        self.regels.append(p.replace("%s",label))
                    if self.nieuwAlbum:
                        self.regels.append(p.replace("%s",""))
                elif x[5:9] == "jaar":
                    # <!-- jaar      <input type="text" name="txtJaar" id="txtJaar" size="6" maxlength="6" value="%s" /> -->
                    p = x[10:]
                    p = p[:-4]
                    if jaar != "":
                        self.regels.append(p.replace("%s",jaar))
                    if self.nieuwAlbum:
                        self.regels.append(p.replace("%s",""))
                elif x[5:12] == "locatie":
                    # <!-- locatie     <input type="text" name="txtLoc" id="txtLoc" size="20" maxlength="80" value="%s"/> -->
                    #~ if self.wijzigO:
                    p = x[13:]
                    p = p[:-4]
                    if locatie != "":
                        self.regels.append(p.replace("%s",locatie))
                    if self.nieuwAlbum:
                        self.regels.append(p.replace("%s",""))
                    #~ else:
                        #~ self.regels.append('    <select name="selTitel" id="selTitel">')
                        #~ for x in lh.Items:
                            #~ if x[2] == locatie.encode("ISO-8859-1") and x[3] == datum.encode("ISO-8859-1"):
                                #~ self.regels.append('    <option selected value="%s">%s %s</option>' % (x[0],x[2],x[3]))
                            #~ else:
                                #~ self.regels.append('    <option value="%s">%s %s</option>' % (x[0],x[2],x[3]))
                        #~ self.regels.append("    </select>")
                        #~ self.regels.append(" <-- selecteer desgewenst een ander concert om te bekijken")
                elif x[5:10] == "datum":
                    # <!-- datum      <input type="text" name="txtDatum" id="txtDatum" size="20" maxlength="20" value="%s" /> -->
                    #~ if self.wijzigO:
                    p = x[11:]
                    p = p[:-4]
                    if datum != "":
                        self.regels.append(p.replace("%s",datum))
                    if self.nieuwAlbum:
                        self.regels.append(p.replace("%s",""))
                elif x[:-1] == '<!-- producer -->':
                    inProd = True
                    inProdLines = []
                elif x[:-1] == '<!-- endproducer -->':
                    inProd = False
                    if len(inProdLines) == 0: inProdLines = [""]
                    for y in inProdLines:
                        if y.find('%s') >= 0:
                            self.regels.append(y % producer)
                        else:
                            self.regels.append(y)
                elif x[5:13] == "producer" and producer != "":
                    # <!-- producer --> 14
                    p = x[14:]
                    p = p[:-4]
                    self.regels.append(p.replace("%s",producer))
                elif x[:-1] == '<!-- credits -->':
                    inCred = True
                    inCredLines = []
                elif x[:-1] == '<!-- endcredits -->':
                    inCred = False
                    if len(inCredLines) == 0: inCredLines = [""]
                    for y in inCredLines:
                        if y.find('%s') >= 0:
                            self.regels.append(y % credits)
                        else:
                            self.regels.append(y)
                elif x[5:12] == "credits" and credits != "":
                    # <!-- credits --> 13
                    p = x[13:]
                    p = p[:-4]
                    self.regels.append(p.replace("%s",credits))
                elif x[:-1] == '<!-- bezetting -->':
                    inBezet = True
                    inBezetLines = []
                elif x[:-1] == '<!-- endbezetting -->':
                    inBezet = False
                    if len(inBezetLines) == 0: inBezetLines = ['']
                    for y in inBezetLines:
                        if y.find('%s') >= 0:
                            self.regels.append(y % bezetting)
                        else:
                            self.regels.append(y)
                elif x[5:14] == "bezetting" and bezetting != "":
                    # <!-- bezetting --> 15
                    p = x[15:]
                    p = p[:-4]
                    self.regels.append(p.replace("%s",bezetting))
                elif x[5:11] == "nummer":
                    # <!-- nummer titel    <option value="%s">%s</option>         -->
                    p = x[18:]
                    p = p[:-4]
                    for y in tracks:
                        pp = p.replace("%s",str(tracknr),1)
                        self.regels.append(pp.replace("%s",y,1))
                        tracknr = tracknr + 1
                elif x[5:19] == 'startTrackList':
                    TrackListLines = True
                    tr_regels = []
                elif x[5:17] == 'endTrackList':
                    TrackListLines = False
                    self.regels.append(tr_regels[0])
                    self.regels.append(tr_regels[1])
                    self.regels.append(tr_regels[2])
                    self.regels.append(tr_regels[3])
                    self.regels.append(tr_regels[4])
                    for y in tracks:
                        self.regels.append(tr_regels[5] % cgipad)
                        self.regels.append(tr_regels[6] % str(tracknr))
                        self.regels.append(tr_regels[7])
                        self.regels.append(tr_regels[8] % self.Id)
                        self.regels.append(tr_regels[9] % self.albumtype)
                        self.regels.append(tr_regels[10] % str(tracknr))
                        self.regels.append(tr_regels[11] % (str(tracknr),y))
                        self.regels.append(tr_regels[12])
                        self.regels.append(tr_regels[13])
                        self.regels.append(tr_regels[14])
                        tracknr = tracknr + 1
                    self.regels.append(tr_regels[15])
                elif x[5:7] == "nr":
                    # <!-- nr soort rest  <option value="%s">%s%s</option>         -->
                    p = x[18:]
                    p = p[:-4]
                    for y in opnames:
                        pp = p.replace("%s",str(opnamenr),1)
                        self.regels.append(pp.replace("%s",y,1))
                        opnamenr = opnamenr + 1
                elif x[5:17] == 'startOpnList':
                    OpnListLines = True
                    op_regels = []
                elif x[5:15] == 'endOpnList':
                    OpnListLines = False
                    self.regels.append(op_regels[0])
                    self.regels.append(op_regels[1])
                    self.regels.append(tr_regels[2])
                    for y in opnames:
                        self.regels.append(op_regels[3] % str(opnamenr))
                        self.regels.append(op_regels[4])
                        self.regels.append(op_regels[5])
                        self.regels.append(op_regels[6] % self.Id)
                        self.regels.append(op_regels[7] % self.albumtype)
                        self.regels.append(op_regels[8] % str(opnamenr))
                        self.regels.append(op_regels[9] % (str(opnamenr),y))
                        self.regels.append(op_regels[10])
                        self.regels.append(op_regels[11])
                        self.regels.append(op_regels[12])
                        opnamenr = opnamenr + 1
                    self.regels.append(op_regels[13])
                elif x[5:12] == "wijzigO":
                    # <!-- wijzigO <input type="hidden" name="hWijzig" value="%s"> -->
                    p = x[13:]
                    p = p[:-4]
                    if self.wijzigO != 1:
                        self.regels.append(p.replace("%s","0"))
                    else:
                        self.regels.append(p.replace("%s","1"))
            elif xh[0] == "-->": continue
            else:
                if inProd:
                    inProdLines.append(x[:-1])
                elif inCred:
                    inCredLines.append(x[:-1])
                elif inBezet:
                    inBezetLines.append(x[:-1])
                elif TrackListLines:
                    tr_regels.append(x[:-1])
                elif OpnListLines:
                    op_regels.append(x[:-1])
                elif x.find("selAlbum") >= 0:
                    self.regels.append('<input type="hidden" name="hType" value="%s" />' % self.albumtype)
                    self.regels.append('<input type="hidden" name="hSZoek" value="%s" />' % self.sZoek)
                    self.regels.append('<input type="hidden" name="hTZoek" value="%s" />' % self.tZoek)
                    self.regels.append('<input type="hidden" name="hSort" value="%s" />' % self.Sort)
                    self.regels.append(x[:-1])
                elif x.find("selecteer titel") >= 0:
                    self.regels.append(x[:-1])
                    for y in lh.Items:
                        self.regels.append('    <option value="%s">%s</option>' % (y[0],y[2]))
                else:
                    self.regels.append(x[:-1])

    def meldfout(self,melding):
        self.regels.append('<html><head><link rel="stylesheet" href="%sfilms.css" type="text/css"></head>' % htmlpad)
        self.regels.append('<body><h1>Albert Muziek!</h1><hr />%s</body></html>' % melding)

if __name__ == '__main__':
    dm = detail_main("studio",0,"44")
    dm.toon()
    f = file("test.html","w")
    for x in dm.regels:
        f.write("%s\n" % x)
    f.close()

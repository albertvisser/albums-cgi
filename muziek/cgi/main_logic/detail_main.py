import os
import globals
from artiest import Artiest, artiestenlijst
from studio import Album, albumlist
from live import Concert, concertlist

fouttekst = """\
<html><head><link rel="stylesheet" href="%sfilms.css" type="text/css"></head>
<body><h1>Albert Muziek!</h1><hr />%s</body></html>
"""
hidden_inputs = """\
<input type="hidden" name="hType" value="%s" />
<input type="hidden" name="hSZoek" value="%s" />
<input type="hidden" name="hTZoek" value="%s" />
<input type="hidden" name="hSort" value="%s" />
"""
option_text = '    <option %s value="%s">%s</option>'
artiest_selector = [
    '    <select name="selArtiest" id="selArtiest">',
    '  ' + option_text,
    "    </select>",
    ]

class Detail(object):
    def __init__(self, typ, wijzig=False, albumid=""):
        self.regels = []
        if typ == 'studio' or typ == 'live':
            self.albumtype = typ
        else:
            self.meldfout("Geen albumtype opgegeven")
            return
        self.wijzigen = wijzig
        if albumid:
            self.id = albumid
        elif self.albumtype == 'studio':
            dh = Album(0)
            self.id = dh.id
        elif self.albumtype == 'live':
            dh = Concert(0)
            self.id = dh.id
        self.nieuw_album = False
        self.artiest = self.titel = self.bezetting = ""
        self.zoeksoort = self.zoektekst = self.sortering = ""
        if self.albumtype == 'studio':
            self.label = self.jaar = self.produced = self.credits = self.volgnr = ""
        elif self.albumtype == 'live':
            self.locatie = self.datum = ""
        self.tracks = []
        self.opnames = []

    def set_arg(self,x,y):
        if x == "albumid":
            if y != 0:
                self.id = y
            elif self.albumtype == 'studio':
                dh = Album(0)
                self.id = dh.id
            elif self.albumtype == 'live':
                dh = Concert(0)
                self.id = dh.id
        elif x == "wijzigO":
            self.wijzigO = y
        elif x == "nieuw":
            self.nieuw_album = y
        ## elif x == "artiest":
            ## self.Artiest = y
        ## elif x == "titel":
            ## self.Titel = y
        ## elif x == "label":
            ## self.Label = y
        ## elif x == "jaar":
            ## self.Jaar = y
        ## elif x == "producer":
            ## self.Produced = y
        ## elif x == "credits":
            ## self.Credits = y
        ## elif x == "bezetting":
            ## self.Bezetting = y
        ## elif x == "locatie":
            ## self.locatie = y
        ## elif x == "datum":
            ## self.datum = y
        ## elif x == "volgnr":
            ## self.volgnr = y
        ## elif x == "tracks":
            ## self.Tracks = y
        ## elif x == "opnames":
            ## self.Opnames = y
        elif x == "tracks":
            for z in y.split("\n"):
                self.tracks.append(z)
        elif x == "opnames":
            for z in y.split("\n"):
                self.opnames.append(z)

    def wijzig(self):
        self.ok = True
        if self.artiest == "":
            self.regels.append(fouttekst % (globals.htmlpad,
                "wijzigen niet mogelijk, artiestnaam onbekend"))
            return
        if self.titel != "":
            self.regels.append(fouttekst % (globals.htmlpad,
                "wijzigen niet mogelijk, titel onbekend"))
            return
        if self.albumtype == 'studio':
            dh = Album(self.id)
        elif self.albumtype == 'live':
            dh = Concert(self.id)
        dh.read()
        dh.artiest = self.artiest
        dh.titel = self.titel.replace("&","&amp;")
        if self.label:
            dh.label = self.label.replace("&","&amp;")
        if self.jaar:
            dh.jaar = self.jaar
        if self.produced:
            dh.producer = self.produced.replace("&","&amp;")
        if self.credits:
            dh.credits = self.credits.replace("&","&amp;")
        if self.bezetting:
            dh.bezetting = self.bezetting.replace("&","&amp;")
        if self.tracks:
            trks = self.tracks.split("\n")
            for y in dh.tracks:
                dh.rem_track(y)
            for y in trks:
                dh.add_track(y.rstrip().replace("&","&amp;"))
        if self.opnames:
            opn = self.opnames.split("\n")
            # hier is het ingewikkelder omdat het eerste deel van de tekst
            # bestaat uit een waarde die eigenlijk uit een selectielijst moet komen
        dh.write()

    def toon(self):
        if self.albumtype == 'studio':
            ih = Album(self.id)
            fnaam = "detail.html"
        elif self.albumtype == 'live':
            ih = Concert(self.id)
            fnaam = "detail_live.html"
        else:
            self.regels.append(fouttekst % (globals.htmlpad,
                "Geen albumtype opgegeven"))
            return
        ih.read()
        if not ih.found:
            self.regels.append(fouttekst % (globals.htmlpad,
                "Album-gegevens niet aanwezig"))
            return
        artiest = ih.artiest
        dh = Artiest(ih.artiest, '0')
        titel = label = jaar = volgnr = producer = credits = locatie = datum = ""
        itemlist = []
        if self.albumtype == 'studio':
            titel = ih.titel
            label = ih.label
            jaar = ih.jaar
            volgnr = ih.volgnr
            producer = ih.producer
            credits = ih.credits
            itemlist = albumlist(['artiest','titel'],{"artiest": dh.id})
        if self.albumtype == 'live':
            locatie = ih.locatie
            datum = ih.datum
            itemlist = concertlist(['artiest','locatie','datum'],{"artiest": dh.id})
        bezetting = ih.bezetting
        tracks = ih.tracks
        opnames = ih.opnames

        spc = ' '
        tracknr = 1
        opnamenr = 1
        in_tracklist = in_opnamelist = in_prod = in_cred = in_bezet = False
        namen = artiestenlijst()
        with open(os.path.join(globals.htmlpad, fnaam)) as fh:
            for x in fh.readlines():
                x = x.rstrip()
                xh = x.split()
                if xh[0] == "<!--":
                    if len(xh) == 1:
                        continue
                    if xh[1] == "kop":
                        for x in globals.kop("detail", self.albumtype,
                                self.zoeksoort, self.zoektekst, self.sortering):
                            self.regels.append(x)
                    elif xh[1] == "artiest":
                        # <!-- artiest   <input type="text" name="txtArtiest" id="txtArtiest" size="20" maxlength="60" value="%s"/><br /> -->
                        self.regels.append(artiest_selector[0])
                        for y in namen:
                            hlp = 'selected="selected"' if y[1] == artiest.encode(
                                "ISO-8859-1") else ''
                            self.regels.append(artiest_selector[1] % (hlp, y[0],
                                y[1]))
                        self.regels.append(artiest_selector[2])
                    elif xh[1] == "titel":
                        #~ <!-- titel     <input type="text" name="txtTitel" id="txtTitel" size="60" maxlength="80" value="%s" /> -->
                        self.regels.append(spc.join(xh[2:-1]) % titel)
                    elif xh[1] == "id":
                        # <!-- id hIdAlbum <input type="hidden" name="hWijzig" id="hWijzig" value="%s" /> -->
                        self.regels.append('   ' + spc.join(xh[3:-1]).replace(
                            'hWijzig', xh[2]) % self.id)
                    elif xh[1] == "type":
                        # <!-- type hTypeAlbum <input type="hidden" name="hWijzig" id="hWijzig" value="%s" /> -->
                        self.regels.append('   ' + spc.join(xh[3:-1]).replace(
                            'hWijzig', xh[2]) % self.albumtype)
                    elif xh[1] == "update":
                        # <!-- update      <input type="submit" abled value="Tracks aanpassen" /> -->
                        hlp = 'disabled="disabled"' if self.nieuw_album else ''
                        self.regels.append('   ' + spc.join(xh[2:-1]).replace(
                            'abled', hlp))
                    elif xh[1] == "label":
                        # <!-- label     <input type="text" name="txtLabel" id="txtLabel" size="20" maxlength="80" value="%s"/><br /> -->
                        self.regels.append('   ' + spc.join(xh[2:-1]) % label)
                    elif xh[1] == "jaar":
                        # <!-- jaar      <input type="text" name="txtJaar" id="txtJaar" size="6" maxlength="6" value="%s" /> -->
                        self.regels.append('   ' + spc.join(xh[2:-1]) % jaar)
                    elif xh[1] == "locatie":
                        # <!-- locatie     <input type="text" name="txtLoc" id="txtLoc" size="20" maxlength="80" value="%s"/> -->
                        self.regels.append('   ' + spc.join(xh[2:-1]) % locatie)
                    elif xh[1] == "datum":
                        # <!-- datum      <input type="text" name="txtDatum" id="txtDatum" size="20" maxlength="20" value="%s" /> -->
                        self.regels.append('   ' + spc.join(xh[2:-1]) % datum)
                    elif xh[1] == 'producer':
                        in_prod = True
                        prod_lines = []
                    elif xh[1] == 'endproducer':
                        in_prod = False
                        if len(prod_lines) == 0:
                            prod_lines = [""]
                        for y in prod_lines:
                            if '%s' in y:
                                self.regels.append(y % producer)
                            else:
                                self.regels.append(y)
                    ## elif xh[1] == "producer" and producer != "":
                        ## # <!-- producer --> 14
                        ## p = x[14:]
                        ## p = p[:-4]
                        ## self.regels.append(p.replace("%s",producer))
                    elif xh[1] == 'credits':
                        in_cred = True
                        cred_lines = []
                    elif xh[1] == 'endcredits':
                        in_cred = False
                        if len(cred_lines) == 0:
                            cred_lines = [""]
                        for y in cred_lines:
                            if '%s' in y:
                                self.regels.append(y % credits)
                            else:
                                self.regels.append(y)
                    ## elif xh[1] == "credits" and credits != "":
                        ## # <!-- credits --> 13
                        ## p = x[13:]
                        ## p = p[:-4]
                        ## self.regels.append(p.replace("%s",credits))
                    elif xh[1] == 'bezetting':
                        in_bezet = True
                        bezet_lines = []
                    elif xh[1] == 'endbezetting':
                        in_bezet = False
                        if len(bezet_lines) == 0:
                            bezet_lines = ['']
                        for y in bezet_lines:
                            if '%s' in y:
                                self.regels.append(y % bezetting)
                            else:
                                self.regels.append(y)
                    ## elif xh[1] == "bezetting" and bezetting != "":
                        ## # <!-- bezetting --> 15
                        ## p = x[15:]
                        ## p = p[:-4]
                        ## self.regels.append(p.replace("%s",bezetting))
                    ## elif xh[1] == "nummer":
                        ## # <!-- nummer titel    <option value="%s">%s</option>         -->
                        ## p = x[18:]
                        ## p = p[:-4]
                        ## for y in tracks:
                            ## pp = p.replace("%s",str(tracknr),1)
                            ## self.regels.append(pp.replace("%s",y,1))
                            ## tracknr = tracknr + 1
                    elif xh[1] == 'startTrackList':
                        in_tracklist = True
                        tr_regels = []
                    elif xh[1] == 'endTrackList':
                        in_tracklist = False
                        self.regels.append(tr_regels[0])
                        self.regels.append(tr_regels[1])
                        self.regels.append(tr_regels[2])
                        self.regels.append(tr_regels[3])
                        self.regels.append(tr_regels[4])
                        for y in tracks:
                            self.regels.append(tr_regels[5] % globals.cgipad)
                            self.regels.append(tr_regels[6] % str(tracknr))
                            self.regels.append(tr_regels[7])
                            self.regels.append(tr_regels[8] % self.id)
                            self.regels.append(tr_regels[9] % self.albumtype)
                            self.regels.append(tr_regels[10] % str(tracknr))
                            self.regels.append(tr_regels[11] % (str(tracknr), y))
                            self.regels.append(tr_regels[12])
                            self.regels.append(tr_regels[13])
                            self.regels.append(tr_regels[14])
                            tracknr = tracknr + 1
                        self.regels.append(tr_regels[15])
                    ## elif xh[1] == "nr":
                        ## # <!-- nr soort rest  <option value="%s">%s%s</option>         -->
                        ## p = x[18:]
                        ## p = p[:-4]
                        ## for y in opnames:
                            ## pp = p.replace("%s",str(opnamenr),1)
                            ## self.regels.append(pp.replace("%s",y,1))
                            ## opnamenr = opnamenr + 1
                    elif xh[1] == 'startOpnList':
                        in_opnamelist = True
                        op_regels = []
                    elif xh[1] == 'endOpnList':
                        in_opnamelist = False
                        self.regels.append(op_regels[0])
                        self.regels.append(op_regels[1])
                        self.regels.append(tr_regels[2])
                        for y in opnames:
                            self.regels.append(op_regels[3] % str(opnamenr))
                            self.regels.append(op_regels[4])
                            self.regels.append(op_regels[5])
                            self.regels.append(op_regels[6] % self.id)
                            self.regels.append(op_regels[7] % self.albumtype)
                            self.regels.append(op_regels[8] % str(opnamenr))
                            self.regels.append(op_regels[9] % (str(opnamenr), y))
                            self.regels.append(op_regels[10])
                            self.regels.append(op_regels[11])
                            self.regels.append(op_regels[12])
                            opnamenr = opnamenr + 1
                        self.regels.append(op_regels[13])
                    elif xh[1] == "wijzigO":
                        # <!-- wijzigO <input type="hidden" name="hWijzig" value="%s"> -->
                        hlp = "1" if self.wijzigen else "0"
                        self.regels.append('    ' + spc.join(xh[2:-1]) % hlp)
                ## elif xh[0] == "-->":
                    ## continue
                else:
                    if in_prod:
                        prod_lines.append(x)
                    elif in_cred:
                        cred_lines.append(x)
                    elif in_bezet:
                        bezet_lines.append(x)
                    elif in_tracklist:
                        tr_regels.append(x)
                    elif in_opnamelist:
                        op_regels.append(x)
                    elif "selAlbum" in x:
                        self.regels.append(hidden_inputs % (self.albumtype,
                            self.zoeksoort, self.zoektekst, self.sortering))
                        self.regels.append(x)
                    elif "selecteer titel" in x:
                        self.regels.append(x)
                        for y in itemlist:
                            self.regels.append(option_text % ('', y[0], y[2]))
                    else:
                        self.regels.append(x)

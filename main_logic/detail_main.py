import os
import globals
from artiest import Artiest, artiestenlijst
from studio import Album, albumlist
from live import Concert, concertlist

fouttekst = """\
<html><head><link rel="stylesheet" href="/muziek.css" type="text/css"></head>
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
        self.artiestid = self.artiest = self.titel = self.bezetting = ""
        self.zoeksoort = self.zoektekst = self.sortering = ""
        if self.albumtype == 'studio':
            self.label = self.jaar = self.producer = self.credits = self.volgnr = ""
        elif self.albumtype == 'live':
            self.locatie = self.datum = ""
        self.tracks = []
        self.trackid, self.tracknaam = None, ''
        self.opnames = []
        self.opnameid, self.opnamenaam = None, ''

    def set_arg(self,x,y):
        if y is None:
            return
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
        elif x == "tracks":
            for z in y.split("\n"):
                self.tracks.append(z)
        elif x == "opnames":
            for z in y.split("\n"):
                self.opnames.append(z)

    def wijzig(self):
        self.regels = []
        self.ok = True
        if self.albumtype == 'studio':
            dh = Album(self.id)
        elif self.albumtype == 'live':
            dh = Concert(self.id)
        dh.read()
        if self.artiestid:
            dh.artiestid = self.artiestid #.replace("&","&amp;")
        if self.albumtype == 'studio':
            if self.titel:
                dh.titel = self.titel.replace("&","&amp;")
            if self.label:
                dh.label = self.label.replace("&","&amp;")
            if self.jaar:
                dh.jaar = self.jaar
            if self.producer:
                dh.producer = self.producer.replace("&","&amp;")
            if self.credits:
                dh.credits = self.credits.replace("&","&amp;")
        elif self.albumtype == 'live':
            if self.locatie:
                dh.locatie = self.locatie.replace("&","&amp;")
            if self.datum:
                dh.datum = self.datum.replace("&","&amp;")
        if self.bezetting:
            dh.bezetting = self.bezetting.replace("&","&amp;")
        if self.trackid is not None:
            if self.trackid == 0: # new track
                dh.add_track(self.tracknaam)
            else:
                dh.tracks[self.trackid - 1] = self.tracknaam
        if self.opnameid is not None:
            if self.opnameid == 0: # new opname
                dh.add_opname(self.opnameoms)
            else:
                dh.opnames[self.opnameid - 1] = self.opnameoms
        dh.write()

    def toon(self, nieuw=False):
        self.regels = []
        if self.albumtype == 'studio':
            ih = Album(self.id)
            fnaam = "detail.html"
        elif self.albumtype == 'live':
            ih = Concert(self.id)
            fnaam = "detail_live.html"
        else:
            self.regels.append(fouttekst % "Geen albumtype opgegeven")
            return
        if not nieuw:
            ih.read()
            if not ih.found:
                self.regels.append(fouttekst % "Album-gegevens niet aanwezig")
                return
        artiestid = ih.artiestid
        artiest = ih.artiest
        titel = label = jaar = volgnr = producer = credits = locatie = datum = ""
        itemlist = []
        if self.albumtype == 'studio':
            titel = ih.titel
            label = ih.label
            jaar = ih.jaar
            volgnr = ih.volgnr
            producer = ih.producer
            credits = ih.credits
            itemlist = albumlist(['artiest', 'titel'], {"artiest": ih.artiestid})
        if self.albumtype == 'live':
            locatie = ih.locatie
            datum = ih.datum
            itemlist = concertlist(['artiest', 'locatie', 'datum'], {"artiest":
                ih.artiestid})
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
                            hlp = 'selected="selected"' if y[1] == artiest else ''
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
                        self.regels.append(tr_regels[15] % globals.cgipad)
                        self.regels.append(tr_regels[16])
                        self.regels.append(tr_regels[17])
                        self.regels.append(tr_regels[18] % self.id)
                        self.regels.append(tr_regels[19] % self.albumtype)
                        self.regels.append(tr_regels[20])
                        self.regels.append(tr_regels[21])
                        self.regels.append(tr_regels[22])
                        self.regels.append(tr_regels[23])
                        self.regels.append(tr_regels[24])
                        self.regels.append(tr_regels[25])
                    elif xh[1] == 'startOpnList':
                        in_opnamelist = True
                        op_regels = []
                    elif xh[1] == 'endOpnList':
                        in_opnamelist = False
                        self.regels.append(op_regels[0])
                        self.regels.append(op_regels[1])
                        self.regels.append(op_regels[2])
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
                        self.regels.append(op_regels[14])
                        self.regels.append(op_regels[15])
                        self.regels.append(op_regels[16] % self.id)
                        self.regels.append(op_regels[17] % self.albumtype)
                        self.regels.append(op_regels[18])
                        self.regels.append(op_regels[19])
                        self.regels.append(op_regels[20])
                        self.regels.append(op_regels[21])
                        self.regels.append(op_regels[22])
                        self.regels.append(op_regels[23])
                    elif xh[1] == "wijzigO":
                        # <!-- wijzigO <input type="hidden" name="hWijzig" value="%s"> -->
                        hlp = "1" if self.wijzigen else "0"
                        self.regels.append('    ' + spc.join(xh[2:-1]) % hlp)
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

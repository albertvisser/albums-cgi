import sys
sys.path.append("F:\\pythoneer\\muziek\\data")
from muziek_studio_met import AlbumList
from muziek_studio_met import Album
from muziek_live_met import ConcertList
from muziek_live_met import Concert
from muziek_artiest import Artiest
from muziek_artiest import ArtiestenLijst

class getArtiesten:
    "lees de artiestentabel"

    def __init__(self):
        dh = ArtiestenLijst()
        self.ArtiestIds = []
        self.ArtiestNamen = []
        self.ArtiestSortkeys = []
        for y in dh.Namen:
            self.ArtiestIds.append(y[0])
            self.ArtiestNamen.append(y[1])
            self.ArtiestSortkeys.append(y[2])

class getSelection:
    "Doe een selectie op het "
    "input:"
    "  type: studio of live"
    "  which: subelement of attrubuut om op te selecteren"
    "  what: selectiewaarde"
    "  how: subelement of attribuut om op te sorteren"
    "geeft terug:"
    "  self.sellist: in scherm te tonen lijst gegevens"
    "  self.keylist: lijst met id's"

    def __init__(self,type,which,what,how):
        self.type = type
        self.which = which
        self.what = what
        self.how = how
        selection = {}
        self.sellist = []
        self.keylist = []

        if which != "niks":
            selection[which] = what
        if which == "artiest":
            ah = Artiest(what,'0')
            selection[which] = ah.Id

        if type == "studio":
            list = ['artiest','titel']
            if how == 'jaar':
                list.append('jaar')
                list.append('volgnr')
        if type == "live":
            list = ['artiest','locatie','datum']

        if len(selection) > 0:
            if type == "studio":
                self.fl = AlbumList(list, selection)
            if type == "live":
                self.fl = ConcertList(list, selection)
        else:
            if type == "studio":
                self.fl = AlbumList(list)
            if type == "live":
                self.fl = ConcertList(list)

        if len(self.fl.Items) > 0:
            self.sort()

    def sort(self):
        sortList = []
        sl = []

        # sorteren en weer te geven lijst samenstellen
        if self.type == "studio":
            if self.how == 'titel':
                for x in self.fl.Items:
                    y = x[2] + ";#;" + x[1] + ";#;" + x[0]
                    sortList.append(y)
                sortList.sort()
                for x in sortList:
                    y = x.split(";#;")
                    z = [y[2],y[1],y[0]]
                    sl.append(z)
            elif self.how == 'jaar':
                for x in self.fl.Items:
                    y = x[3] + x[4] + ";#;" + x[2] + ";#;" + x[1] + ";#;" + x[0]
                    sortList.append(y)
                sortList.sort()
                for x in sortList:
                    y = x.split(";#;")
                    z = [y[3],y[2],y[1]]
                    sl.append(z)
            elif self.how == 'artiest':
                # via de aparte sorteersleutel
                for x in self.fl.Items:
                    ah = Artiest(x[1].decode('ISO-8859-1'), '0')
                    y = ah.sort + ";#;" + x[2] + ";#;" + x[1] + ";#;" + x[0]
                    sortList.append(y)
                sortList.sort()
                for x in sortList:
                    y = x.split(";#;")
                    z = [y[3],y[2],y[1]]
                    sl.append(z)
            else:
                for x in self.fl.Items:
                    y = [x[0], x[1], x[2]]
                    sl.append(y)
            for y in sl:
                if self.which == 'opname':
                #   Items bestaat uit id, artiest, titel en loc
                    h = ('%s - %s (%s)' % (y[1],y[2],y[3]))
                else:
                #   Items bestaat uit id, artiest en titel
                    h = ('%s - %s' % (y[1],y[2]))
                self.sellist.append(h)
                self.keylist.append(y[0])
        if self.type == "live":
            if self.how == "plaats":
                for x in self.fl.Items:
                    y = x[2] + ";#;" + x[3] + ";#;" + x[1] + ";#;" + x[0]
                    sortList.append(y)
                sortList.sort()
                for x in sortList:
                    y = x.split(";#;")
                    z = [y[4],y[3],y[1],y[2]]
                    sl.append(z)
            elif self.how == "datum":
                for x in self.fl.Items:
                    y = x[3] + ";#;" + x[1] + ";#;" + x[2] + ";#;" + x[0]
                    sortList.append(y)
                sortList.sort()
                for x in sortList:
                    y = x.split(";#;")
                    z = [y[3],y[1],y[2],y[0]]
                    sl.append(z)
            elif self.how == 'artiest':
                # via de aparte sorteersleutel
                for x in self.fl.Items:
                    ah = Artiest(x[1], '0')
                    y = ah.sort + ";#;" + x[2] + ";#;" + x[3] + ";#;" + x[1] + ";#;" + x[0]
                    sortList.append(y)
                sortList.sort()
                for x in sortList:
                    y = x.split(";#;")
                    z = [y[4],y[3],y[1],y[2]]
                    sl.append(z)
            else:
                for x in self.fl.Items:
                    y = [x[0], x[1], x[2], x[3]]
                    sl.append(y)
            for y in sl:
                if  self.which == 'opname':
                #   Items bestaat uit id, artiest, titel en loc
                    h = ('%s - %s, %s (%s)' % (y[1],y[2],y[3],y[4]))
                else:
                #   Items bestaat uit id, artiest en titel
                    h = ('%s - %s, %s' % (y[1],y[2],y[3]))
                self.sellist.append(h)
                self.keylist.append(y[0])

class getDetail:
    "Zoek een album op in het betreffende bestand"
    "input:"
    "  type: studio of live"
    "  key: sleutel van het te tonen item (0 = nieuwe)"
    "geeft terug:"
    "  self.sellist: in scherm te tonen lijst gegevens"
    "  self.keylist: lijst met id's"

    def __init__(self,type,key):

        if type == 'studio': ih = Album(key)
        if type == 'live': ih = Concert(key)

        if key != 0:
            ih.read()
##            if ih.found:

        self.artiest = ih.Artiest
        if type == 'studio':
            self.titel = ih.Titel
            self.label = ih.Label
            self.jaar = ih.Jaar
            self.volgnr = ih.Volgnr
            self.producer = ih.Producer
            self.credits = ih.Credits
        if type == 'live':
            self.locatie = ih.Locatie
            self.datum = ih.Datum
        self.bezetting = ih.Bezetting
        self.tracks = ih.Tracks
        self.opnames = ih.Opnames

    def setProp(self,property,value):

        if property == "artiest":
            self.artiest = value
        elif property == "titel":
            self.titel = value
        elif property == "label":
            self.label = value
        elif property == "jaar":
            self.jaar = value
        elif property == "volgnr":
            self.volgnr = value
        elif property == "producer":
            self.producer = value
        elif property == "credits":
            self.credits = value
        elif property == "locatie":
            self.locatie = value
        elif property == "datum":
            self.datum = value
        elif property == "bezetting":
            self.bezetting = value

##    def addTrack(self,Track):
##    def remTrack(self,Track):
##    def editTrack(self,oldTrack,newTrack):
##    def insTrack(self,oldTrack,newTrack): #        "let op: insert BEFORE"
##    def addOpname(self,Opname):
##    def remOpname(self,Opname):

class setArtiest:

    def __init__(self,Id,naam,sort):
        ah = Artiest(Id)
        if Id != 0:
            ah.read()
        if naam != ah.Naam:
            ah.setNaam(naam)
        if sort != ah.sort:
            ah.setSort(sort)
        ah.write()

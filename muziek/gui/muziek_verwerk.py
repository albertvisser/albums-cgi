import sys
import collections
sys.path.append("/home/albert/pythoneer/muziek/data")
from studio import Album, albumlist
from live import Concert, concertlist
from artiest import Artiest, artiestenlijst

def lees_artiesten():
    """lees de artiestentabel
    """
    ids = []
    namen = []
    sortkeys = []
    for id, naam, sortkey in artiestenlijst():
        ids.append(id)
        namen.append(naam)
        sortkeys.append(sortkey)
    return ids, namen, sortkeys

def update_artiest(id_, naam, sort):
    """werk artiest bij in artiestentabel
    """
    ah = Artiest(id_)
    if id_ != 0:
        ah.read()
    changed = False
    if naam != ah.naam:
        ah.setNaam(naam)
        changed = True
    if sort != ah.sort:
        ah.setSort(sort)
        changed = True
    if changed:
        ah.write()


def sort_albums(data, how):
    sellist, keylist = [], []
    sortlist = []

    for x in data:
        if how == 'titel':
            y = (x[2], x[1], x[0])
        elif how == 'jaar':
            y = ((x[3], x[4]), x[2], x[1], x[0])
        elif how == 'artiest':
            # via de aparte sorteersleutel
            ah = Artiest(x[1], '0')
            y = (ah.sort, x[2], x[1], x[0])
        else:
            y = (int(x[0]), x[1], x[2])
        sortlist.append(y)

    sortlist.sort()
    sl = []

    for y in sortlist:
        if how == 'titel':
            z = [y[2], y[1], y[0]]
        elif how == 'jaar':
            z = [y[3], y[2], y[1]] # en die laatste en eerste rubriek dan?
        elif how == 'artiest':
            z = [y[3], y[2], y[1]] # eerste rubriek niet nodig
        else:
            z = [y[0], y[1], y[2]]
        sl.append(z)

    for y in sl:
        #   Items bestaat uit id, artiest en titel
        h = ('%s - %s' % (y[1], y[2]))
        sellist.append(h)
        keylist.append(y[0])

    return sellist, keylist


def sort_concerten(data, how):
    sellist, keylist = [], []
    sortlist = []

    for x in data:
        if how == "plaats":
            y = (x[2], x[3], x[1], x[0])
        elif how == "datum":
            y = ([z for z in reversed(x[3].split())], x[1], x[2], x[0])
        elif how == 'artiest':
            # via de aparte sorteersleutel
            ah = Artiest(x[1], '0')
            y = (ah.sort, x[2], x[3], x[1], x[0])
        else:
            y = (int(x[0]), x[1], x[2], x[3])
        sortlist.append(y)

    sortlist.sort()
    sl = []

    for y in sortlist:
        if how == "plaats":
            z = [y[4], y[3], y[1], y[2]]
        elif how == "datum":
            z = [y[3], y[1], y[2], " ".join([x for x in reversed(y[0])])]
        elif how == 'artiest':
            z = [y[4], y[3], y[1], y[2]]
        else:
            z = [y[0], y[1], y[2], y[3]]
        sl.append(z)

    for y in sl:
        #   Items bestaat uit id, artiest, titel en loc
        h = ('%s - %s, %s' % (y[1],y[2],y[3]))
        sellist.append(h)
        keylist.append(y[0])

    return sellist, keylist


def selection(type, which, what, how):
    "Doe een selectie op het "
    "input:"
    "  type: studio of live"
    "  which: subelement of attribuut om op te selecteren"
    "  what: selectiewaarde"
    "  how: subelement of attribuut om op te sorteren"
    "geeft terug:"
    "  sellist: in scherm te tonen lijst gegevens"
    "  keylist: lijst met id's"

    if type not in ('studio', 'live'):
        raise ValueError('Wrong value for albumtype')

    sellist, keylist = [], []
    seldict = {}
    if which == "artiest":
        ah = Artiest(what, '0')
        seldict[which] = ah.id
    elif which != "niks":
        seldict[which] = what

    if type == "studio":
        columns = ['artiest','titel']
        if how == 'jaar':
            columns.append('jaar')
            columns.append('volgnr')
    else: # if type == "live":
        columns = ['artiest','locatie','datum']

    if seldict:
        if type == "studio":
            data = albumlist(columns, seldict)
        else: # if type == "live":
            data = concertlist(columns, seldict)
    else:
        if type == "studio":
            data = albumlist(columns)
        else: # if type == "live":
            data = concertlist(columns)

    if len(data) > 0:
        if type == "studio":
            sellist, keylist = sort_albums(data, how)
        else: # if type == "live":
            sellist, keylist = sort_concerten(data, how)

    return sellist, keylist

class Detail:
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

        self.artiest = ih.artiest
        if type == 'studio':
            self.titel = ih.titel
            self.label = ih.label
            self.jaar = ih.jaar
            self.volgnr = ih.volgnr
            self.producer = ih.producer
            self.credits = ih.credits
        if type == 'live':
            self.locatie = ih.locatie
            self.datum = ih.datum
        self.bezetting = ih.bezetting
        self.tracks = ih.tracks
        self.opnames = ih.opnames

    def set_prop(self,property,value):

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

##    def update(self):
##    def addTrack(self,Track):
##    def remTrack(self,Track):
##    def editTrack(self,oldTrack,newTrack):
##    def insTrack(self,oldTrack,newTrack): #        "let op: insert BEFORE"
##    def addOpname(self,Opname):
##    def remOpname(self,Opname):

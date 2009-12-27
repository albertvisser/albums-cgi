from muziek_studio_met import Album
from muziek_live_met import Concert

def wijzig(item):
    def __init__(self,type,id):
        self.Type = type
        if id != 0:
            self.Id = id
        elif albumtype == 'studio':
            dh = Album(0)
            self.Ud = dh.id
        elif albumtype == 'studio':
            dh = Concert(0)
            self.Id = dh.id
        self.Artiest = ""
        self.Titel = ""
        self.Label = ""
        self.Jaar = ""
        self.Produced = ""
        self.Credits = ""
        self.Bezetting = ""
        self.Tracks = ""
        self.Opnames = ""

    def setAttr(self,x,y):
        if x == "artiest":
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
        elif x == "tracks":
            self.Tracks = y
        elif x == "opnames":
            self.Opnames = y
        #~ elif x == "":
            #~ self. = y

    def pasAan():
        self.ok = True
        if self.Artiest == "":
            self.fout("artiestnaam")
            return
        if self.Titel != "":
            self.fout("titel")
            return
        if self.Type == 'studio':
            dh = Album(self.Id)
        elif self.Type == 'live':
            dh = Concert(self.Id)
        else:
            self.fout("albumtype")
            return
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

    def fout(self,f):
        self.foutregel = ("wijzigen niet mogelijk, %s onbekend" % f)
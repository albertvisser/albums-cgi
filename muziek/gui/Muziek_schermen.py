from Tkinter import *
import tkMessageBox 
import Pmw
from Muziek_verwerk import getArtiesten
from Muziek_verwerk import setArtiest
from Muziek_verwerk import getSelection
from Muziek_verwerk import getDetail

class Startscherm:

    def __init__(self, app):

        self.app = app
        self.master = app.master
        self.selStudio = IntVar()
        self.txtStudio = StringVar()
        self.selLive = IntVar()
        self.txtLive = StringVar()
        self.show()

    def show(self):

        self.fToolbar = Frame(self.app.fKop)
        self.fToolbar.grid(row=0, column=2)
        self.btnExit = Button(self.fToolbar, text="Exit", command=self.master.quit)
        self.btnExit.grid(row=0,column=0,sticky=E)
        self.btnArtiest = Button(self.fToolbar, text="Lijst artiesten / artiest wijzigen", command=self.ArtiestSel)
        self.btnArtiest.grid(row=0,column=2,sticky=W)

        fr = 4

        self.fStudio = Frame(self.master)
        self.fStudio.grid(row=fr, padx=5, pady=5)
        fr = fr + 1
        r = 0
        w = Label(self.fStudio, text="Selecteer studio-albums op:")
        w.grid(row=r,columnspan=3,sticky=W)
        r = r + 1
        self.selectStudioAlles = Radiobutton(self.fStudio, text="1. Niet zoeken, alles tonen", variable=self.selStudio, value=1)
        self.selectStudioAlles.grid(row=r,column=1,columnspan=2,sticky=W)
        r = r + 1
        self.selectStudioUitv = Radiobutton(self.fStudio, text="2. Uitvoerende:", variable=self.selStudio, value=2)
        self.selectStudioUitv.grid(row=r,column=1,sticky=W)
        self.selectStudioArtist = Pmw.ComboBox(self.fStudio,scrolledlist_items = self.app.ArtiestNamen,listbox_bg="#ffffff")
        self.selectStudioArtist.grid(row=r,column=2,sticky=W)
        
        r = r + 1
        self.selectStudioTitel = Radiobutton(self.fStudio, text="3. Titel", variable=self.selStudio, value=3)
        self.selectStudioTitel.grid(row=r,column=1,sticky=W)
        r = r + 1
        self.selectStudioProducer = Radiobutton(self.fStudio, text="4. Producer", variable=self.selStudio, value=4)
        self.selectStudioProducer.grid(row=r,column=1,sticky=W)
        r = r + 1
        self.selectStudioCredits = Radiobutton(self.fStudio, text="5. Vermelding in Credits", variable=self.selStudio, value=5)
        self.selectStudioCredits.grid(row=r,column=1,columnspan=2,sticky=W)
        r = r + 1
        self.selectStudioBezet = Radiobutton(self.fStudio, text="6. Vermelding in Bezetting", variable=self.selStudio, value=6)
        self.selectStudioBezet.grid(row=r,column=1,columnspan=2,sticky=W)
        r = r + 1
        w = Label(self.fStudio, text="Zoektekst voor 3 - 6: ")
        w.grid(row=r,column=1,sticky=W)
        self.StudioSearchText = Entry(self.fStudio, width="60", textvariable=self.txtStudio)
        self.StudioSearchText.grid(row=r,column=2,sticky=W)
        r = r + 1

        w = Label(self.fStudio, text="Sorteer op:")
        w.grid(row=r,column=0, pady=5, sticky=W)
        self.selectStudioSort = Pmw.ComboBox(self.fStudio,scrolledlist_items = ["Uitvoerende", "Titel", "Jaar", "Niets"],listbox_bg="#ffffff")
        self.selectStudioSort.grid(row=r,column=1,columnspan=2,pady=5, sticky=W)
        self.selectStudioSort.selectitem(2, setentry = 1)
        r = r + 1

        self.selStudio.set(2)
        self.selectStudioSort.select_anchor(2)

        self.btnStudio1 = Button(self.fStudio, text="Selectie uitvoeren", command=self.StudioSel)
        self.btnStudio1.grid(row=r,column=1,sticky=W)

        self.btnStudio2 = Button(self.fStudio, text="Nieuw album opvoeren", command=self.StudioNew)
        self.btnStudio2.grid(row=r,column=2,sticky=W)
        r = r + 1

        self.fDivide1 = Frame(self.master, width=800, height=1)
        self.fDivide1.grid(row=fr,columnspan=3)
        fr = fr + 1
        self.fDivide2 = Frame(self.master, width=800, height=1, bg="#000000")
        self.fDivide2.grid(row=fr,columnspan=3)
        fr = fr + 1
        self.fDivide3 = Frame(self.master, width=800, height=1)
        self.fDivide3.grid(row=fr,columnspan=3)
        fr = fr + 1

        self.fLive = Frame(self.master)
        self.fLive.grid(row=fr, padx=5, pady=5)
        fr = fr + 1
        r = 0
        w = Label(self.fLive, text="Selecteer live opnames op:")
        w.grid(row=r,columnspan=3,sticky=W)
        r = r + 1
        self.selectLiveAlles = Radiobutton(self.fLive, text="1. Niet zoeken, alles tonen", variable=self.selLive, value=1)
        self.selectLiveAlles.grid(row=r,column=1,columnspan=2,sticky=W)
        r = r + 1
        self.selectLiveUitv = Radiobutton(self.fLive, text="2. Uitvoerende:", variable=self.selLive, value=2)
        self.selectLiveUitv.grid(row=r,column=1,sticky=W)
        self.selectLiveArtist = Pmw.ComboBox(self.fLive,scrolledlist_items = self.app.ArtiestNamen,listbox_bg="#ffffff")
        self.selectLiveArtist.grid(row=r,column=2,sticky=W)
        r = r + 1
        self.selectLiveLocatie = Radiobutton(self.fLive, text="3. Locatie", variable=self.selLive, value=3)
        self.selectLiveLocatie.grid(row=r,column=1,sticky=W)
        r = r + 1
        self.selectLiveDatum = Radiobutton(self.fLive, text="4. Datum", variable=self.selLive, value=4)
        self.selectLiveDatum.grid(row=r,column=1,sticky=W)
        r = r + 1
        self.selectLiveBezet = Radiobutton(self.fLive, text="5. Vermelding in Bezetting", variable=self.selLive, value=6)
        self.selectLiveBezet.grid(row=r,column=1,columnspan=2,sticky=W)
        r = r + 1
        w = Label(self.fLive, text="Zoektekst voor 3 - 5: ")
        w.grid(row=r,column=1,sticky=W)
        self.LiveSearchText = Entry(self.fLive, width="60", textvariable=self.txtLive)
        self.LiveSearchText.grid(row=r,column=2,sticky=W)
        r = r + 1

        w = Label(self.fLive, text="Sorteer op:")
        w.grid(row=r,column=0,pady=5, sticky=W)
        self.selectLiveSort = Pmw.ComboBox(self.fLive,scrolledlist_items = ["Uitvoerende", "Locatie", "Datum", "Niets"],listbox_bg="#ffffff")
        self.selectLiveSort.grid(row=r,column=1,columnspan=2,pady=5, sticky=W)
        self.selectLiveSort.selectitem(2, setentry = 1)
        r = r + 1

        self.selLive.set(2)
        self.selectLiveSort.select_anchor(2)

        self.btnLive1 = Button(self.fLive, text="Selectie uitvoeren", command=self.LiveSel)
        self.btnLive1.grid(row=r,column=1,sticky=W)
        self.btnLive2 = Button(self.fLive, text="Nieuwe opname opvoeren", command=self.LiveNew)
        self.btnLive2.grid(row=r,column=2,sticky=W)
        r = r + 1

        self.fDivide4 = Frame(self.master, width=800, height=1)
        self.fDivide4.grid(row=fr,columnspan=3)
        fr = fr + 1
        self.fDivide5 = Frame(self.master, width=800, height=1, bg="#000000")
        self.fDivide5.grid(row=fr,columnspan=3)
        fr = fr + 1
        self.fDivide6 = Frame(self.master, width=800, height=1)
        self.fDivide6.grid(row=fr,columnspan=3)
        fr = fr + 1

##        self.fArtiest = Frame(self.master)
##        self.fArtiest.grid(row=fr, padx=5, pady=5, sticky = W)
##        fr = fr + 1
##        r = 0
##
##        w = Label(self.fArtiest, text="Sorteer op:",fg="#c0c0c0")
##        w.grid(row=r,column=0,sticky=W)
##        
##        self.btnArtiest1 = Button(self.fArtiest, text="Nieuwe artiest opvoeren", command=self.ArtiestNew)
##        self.btnArtiest1.grid(row=r,column=1,sticky=W)
##
##        self.btnArtiest2 = Button(self.fArtiest, text="Lijst artiesten / artiest wijzigen", command=self.ArtiestSel)
##        self.btnArtiest2.grid(row=r,column=2,sticky=W)
##        r = r + 1

    def hide(self):
        self.fToolbar.grid_forget()
        self.fStudio.grid_forget()
        self.fDivide1.grid_forget()
        self.fDivide2.grid_forget()
        self.fDivide3.grid_forget()
        self.fLive.grid_forget()
        self.fDivide4.grid_forget()
        self.fDivide5.grid_forget()
        self.fDivide6.grid_forget()
##        self.fArtiest.grid_forget()
##        self.fDivide7.grid_forget()


    def StudioSel(self):
        self.app.starttosel("studio")

    def StudioNew(self):
        self.app.starttodetail("studio")

    def LiveSel(self):
        self.app.starttosel("live")

    def LiveNew(self):
        self.app.starttodetail("live")

    def ArtiestSel(self):
        self.app.starttoart()

    def ArtiestNew(self):
        self.app.starttoartdet()

    def quit(self):
        self.master.quit
        

class Selectiescherm:
    
    def __init__(self,app,type):
        self.app = app
        self.master = app.master
        self.show(type)

    def show(self,type):
        self.Type = type
        tekst1 = "Lijst"
        tekst2 = "Kies"
        if type == "studio":
            tekst1 = "Lijst studio-albums: "
            tekst2 = "Kies een album uit de lijst:"
        if type == "live":
            tekst1 = "Lijst live opnames: "
            tekst2 = "Kies een opname uit de lijst:"
        if self.app.which == "niks":
            tekst1 = tekst1 + "geen selectie; "
        else:
            tekst1 = tekst1 + "selectie op "
            if self.app.which == "artiest":
                tekst1 = tekst1 + self.app.which + ' "' + self.app.what + '"; '
            else:
                tekst1 = tekst1 + ' "' + self.app.what + '" in ' + self.app.which + '; '
        if self.app.how == "Niets":
            tekst1 = tekst1 + "geen sortering"
        else:
            tekst1 = tekst1 + "sortering op " + self.app.how

        self.fToolbar = Frame(self.app.fKop)
        self.fToolbar.grid(row=0, column=2)
        self.btnBack = Button(self.fToolbar, text="Andere selectie", command=self.SeltoStart)
        self.btnBack.grid(row=0,column=0,sticky=E)
        self.btnExit = Button(self.fToolbar, text="Exit", command=self.master.quit)
        self.btnExit.grid(row=0,column=1,sticky=E)

        fr = 4

        self.fTitle = Frame(self.master)
        self.fTitle.grid(row=fr, padx=5, pady=5)
        fr = fr + 1
        r = 0
        w = Label(self.fTitle, text=tekst1)
        w.grid(row=r,columnspan=3,sticky=W)

        self.fDivide1 = Frame(self.master, width=800, height=1)
        self.fDivide1.grid(row=fr,columnspan=3)
        fr = fr + 1
        self.fDivide2 = Frame(self.master, width=800, height=1, bg="#000000")
        self.fDivide2.grid(row=fr,columnspan=3)
        fr = fr + 1
        self.fDivide3 = Frame(self.master, width=800, height=1)
        self.fDivide3.grid(row=fr,columnspan=3)
        fr = fr + 1

        self.fSelect = Frame(self.master)
        self.fSelect.grid(row=fr, padx=5, pady=5)
        fr = fr + 1
        r = 0
        w = Label(self.fSelect, text=tekst2)
        w.grid(row=0,column=0,sticky=NW)
##        self.selectItem = Listbox(self.fSelect,height=20,width=60,bg="#ffffff",exportselection=0)
##        for item in self.app.vh.sellist:
##            self.selectItem.insert(END, item)
        self.selectItem = Pmw.ScrolledListBox(self.fSelect,
                items=self.app.vh.sellist,
##                labelpos='nw',
##                label_text=tekst2,
                listbox_height = 20,
                listbox_width = 60,
                listbox_bg="#ffffff",
                selectioncommand=self.activateSelect,
##                dblclickcommand=self.defCmd,
##                usehullsize = 1,
##                hull_width = 200,
##                hull_height = 200,
        )
        self.selectItem.grid(row=0,column=1,rowspan=2,sticky=W)

        self.btnSelect = Button(self.fSelect, text="Toon gegevens", command=self.SeltoDetail,state=DISABLED)
        self.btnSelect.grid(row=0,column=2,sticky=NW, padx=5, pady=5)
        self.btnNew = Button(self.fSelect, text="Nieuwe opname opvoeren", command=self.SeltoNew)
        self.btnNew.grid(row=1,column=2,sticky=NW,padx=5)

    def activateSelect(self):
        self.btnSelect.config(state=NORMAL)
        
    def hide(self):
        self.fToolbar.grid_forget()
        self.fTitle.grid_forget()
        self.fDivide1.grid_forget()
        self.fDivide2.grid_forget()
        self.fDivide3.grid_forget()
        self.fSelect.grid_forget()
        
    def SeltoDetail(self):
        self.app.seltodetail(self.Type)
        
    def SeltoNew(self):
        self.app.seltodetail(self.Type,1)
        
    def SeltoStart(self):
        self.app.seltostart()


class Detailscherm:
    
    def __init__(self,app,type):
        self.app = app
        self.master = app.master
        self.txtTitel = StringVar()
        self.txtLabel = StringVar()
        self.intJaar = IntVar()
        self.intVolgnr = IntVar()
        self.txtProducer = StringVar()
        self.txtCredits = StringVar()
        self.txtLocatie = StringVar()
        self.txtDatum = StringVar()
        self.txtBezetting = StringVar()
        self.show(type)

    def show(self,type):
        self.Type = type

        self.fToolbar = Frame(self.app.fKop)
        self.fToolbar.grid(row=0, column=2)
        self.btnBacktoSel = Button(self.fToolbar, text="Terug naar selectie", command=self.DettoSel,state=DISABLED)
        self.btnBacktoSel.grid(row=0,column=0,sticky=E)
        self.btnPrevinSel = Button(self.fToolbar, text="Vorige", command=self.DettoDetP,state=DISABLED)
        self.btnPrevinSel.grid(row=0,column=1,sticky=E)
        self.btnNextinSel = Button(self.fToolbar, text="Volgende", command=self.DettoDetN,state=DISABLED)
        self.btnNextinSel.grid(row=0,column=2,sticky=E)
        if self.app.selExists:
            if self.app.ix > 0:
                self.btnPrevinSel.config(state=NORMAL)
            self.btnBacktoSel.config(state=NORMAL)
            if self.app.ix < len(self.app.vh.keylist) - 1:
                self.btnNextinSel.config(state=NORMAL)
        self.btnBacktoStart = Button(self.fToolbar, text="Terug naar startscherm", command=self.DettoStart)
        self.btnBacktoStart.grid(row=0,column=3,sticky=E)
        self.btnExit = Button(self.fToolbar, text="Exit", command=self.master.quit)
        self.btnExit.grid(row=0,column=4,sticky=E)

        fr = 4

        self.fAlbum_show()

        self.fDivide1 = Frame(self.master, width=800, height=1)
        self.fDivide1.grid(row=fr,columnspan=3)
        fr = fr + 1
        self.fDivide2 = Frame(self.master, width=800, height=1, bg="#000000")
        self.fDivide2.grid(row=fr,columnspan=3)
        fr = fr + 1
        self.fDivide3 = Frame(self.master, width=800, height=1)
        self.fDivide3.grid(row=fr,columnspan=3)
        fr = fr + 1

        self.fTracks_show()

        self.fDivide4 = Frame(self.master, width=800, height=1)
        self.fDivide4.grid(row=fr,columnspan=3)
        fr = fr + 1
        self.fDivide5 = Frame(self.master, width=800, height=1, bg="#000000")
        self.fDivide5.grid(row=fr,columnspan=3)
        fr = fr + 1
        self.fDivide6 = Frame(self.master, width=800, height=1)
        self.fDivide6.grid(row=fr,columnspan=3)
        fr = fr + 1

        self.fOpnames_show()

    def fAlbum_show(self):
        fr = 4
        self.fAlbum = Frame(self.master)
        self.fAlbum.grid(row=fr, padx=5, pady=5)
        fr = fr + 1
        r = 0
        
        w = Label(self.fAlbum, text="Album:",width="15")
        w.grid(row=r,column=0,sticky=W)
        self.selectArtist = Pmw.ComboBox(self.fAlbum,scrolledlist_items = self.app.ArtiestNamen,listbox_bg="#ffffff")
        index = 0
        for x in self.app.ArtiestNamen:
            try:
                if x == self.app.dh.artiest:
                    self.selectArtist.selectitem(index, setentry = 1)
                    break
            except:
                pass
            index = index + 1
        self.selectArtist.grid(row=r,column=1,sticky=W)

        if self.Type == "studio":
            self.Titel = Entry(self.fAlbum, width="60", textvariable=self.txtTitel)
            self.Titel.delete(0,END)
            self.Titel.insert(END,self.app.dh.titel)
            self.Titel.grid(row=r,column=2,columnspan=3,sticky=W)
            r = r + 1

            w = Label(self.fAlbum, text="Label/jaar:",width="15")
            w.grid(row=r,column=0,sticky=W)
            self.Label = Entry(self.fAlbum, width="23", textvariable=self.txtLabel)
            self.Label.delete(0,END)
            self.Label.insert(END,self.app.dh.label)
            self.Label.grid(row=r,column=1,sticky=W)
            self.Jaar = Entry(self.fAlbum, width="6", textvariable=self.intJaar)
            self.Jaar.delete(0,END)
            self.Jaar.insert(END,self.app.dh.jaar)
            self.Jaar.grid(row=r,column=2,sticky=W)
            self.Volgnr = Entry(self.fAlbum, width="3", textvariable=self.intVolgnr)
            self.Volgnr.delete(0,END)
            self.Volgnr.insert(END,self.app.dh.volgnr)
            self.Volgnr.grid(row=r,column=3,sticky=W)
            w = Label(self.fAlbum, text=" ",width="51")
            w.grid(row=r,column=4,sticky=NW)
            r = r + 1

            w = Label(self.fAlbum, text="Produced by:",width="15")
            w.grid(row=r,column=0,sticky=W)
            self.Producer = Text(self.fAlbum,width="80",height="2",wrap=WORD)
            self.Producer.delete(1.0,END)
            self.Producer.insert(END,self.app.dh.producer)
            self.Producer.grid(row=r,column=1,columnspan=4,sticky=W)
            r = r + 1

            w = Label(self.fAlbum, text="Credits:",width="15")
            w.grid(row=r,column=0,sticky=W)           
            self.Credits = Text(self.fAlbum,width="80",height="4",wrap=WORD)
            self.Credits.delete(1.0,END)
            self.Credits.insert(END,self.app.dh.credits)
            self.Credits.grid(row=r,column=1,columnspan=4,sticky=W)
            r = r + 1

        if self.Type == "live":
            w = Label(self.fAlbum, text="Plaats/datum:",width="15")
            w.grid(row=r,column=0,sticky=W)
            self.Plaats = Entry(self.fAlbum, width="40", textvariable=self.txtLocatie)
            self.Plaats.delete(0,END)
            self.Plaats.insert(END,self.app.dh.locatie)
            self.Plaats.grid(row=r,column=1,sticky=W)
            self.Datum = Entry(self.fAlbum, width="20", textvariable=self.txtDatum)
            self.Datum.delete(0,END)
            self.Datum.insert(END,self.app.dh.datum)
            self.Datum.grid(row=r,column=2,sticky=W)
##            w = Label(self.fAlbum, text=" ",width="43")
##            w.grid(row=r,column=4,sticky=NW)
            r = r + 1

        self.btnAlbumUpdate = Button(self.fAlbum, text="Gegevens bijwerken", command=self.fAlbumUpdate,state=DISABLED)
        self.btnAlbumUpdate.grid(row=0,column=5,sticky=NW,padx=5)
        self.btnAlbumCancel = Button(self.fAlbum, text="Gegevens terugzetten", command=self.fAlbumCancel,state=DISABLED)
        self.btnAlbumCancel.grid(row=1,column=5,sticky=NW,padx=5)

        w = Label(self.fAlbum, text="Bezetting:",width="15")
        w.grid(row=r,column=0,sticky=W)
        self.Bezetting = Text(self.fAlbum,width="80",height="4",wrap=WORD)
        self.Bezetting.delete(1.0,END)
        self.Bezetting.insert(END,self.app.dh.bezetting)
        self.Bezetting.grid(row=r,column=1,columnspan=4,sticky=W)
        r = r + 1

    def fTracks_show(self):
        fr = 7
        self.fTracks = Frame(self.master)
        self.fTracks.grid(row=fr, padx=5, pady=5)
        fr = fr + 1
        r = 0
        w = Label(self.fTracks, text="Tracks: ",width="15")
        w.grid(row=0,column=0,sticky=NW)
##        self.selectTrack = Listbox(self.fTracks,height=12,width=60,bg="#ffffff",exportselection=0)
##        for item in self.app.vh.sellist:
##            self.selectTrack.insert(END, item)
        self.selectTrack = Pmw.ScrolledListBox(self.fTracks,
                items=self.app.dh.tracks,
                listbox_height = 12,
                listbox_width = 60,
                listbox_bg="#ffffff")
        self.selectTrack.grid(row=0,column=1,rowspan=2,sticky=W)
##        w = Label(self.fTracks, text=" ",width="45")
##        w.grid(row=0,column=2,sticky=NW)

        self.btnTracksUpdate = Button(self.fTracks, text="Trackgegevens bijwerken", command=self.fTracksUpdate,state=DISABLED)
        self.btnTracksUpdate.grid(row=0,column=2,sticky=NW,padx=5,pady=5)
        self.btnTracksCancel = Button(self.fTracks, text="Gegevens terugzetten", command=self.fTracksCancel,state=DISABLED)
        self.btnTracksCancel.grid(row=1,column=2,sticky=NW,padx=5,pady=5)

    def fOpnames_show(self):
        fr = 10
        self.fOpnames = Frame(self.master)
        self.fOpnames.grid(row=fr, padx=5, pady=5)
        fr = fr + 1
        r = 0
        w = Label(self.fOpnames, text="Opgenomen op: ",width="15")
        w.grid(row=0,column=0,sticky=NW)
##        self.selectOpname = Listbox(self.fOpnames,height=5,width=60,bg="#ffffff",exportselection=0)
##        for item in self.app.vh.sellist:
##            self.selectOpname.insert(END, item)
        self.selectOpname = Pmw.ScrolledListBox(self.fOpnames,
                items=self.app.dh.opnames,
                listbox_height = 5,
                listbox_width = 60,
                listbox_bg="#ffffff")
        self.selectOpname.grid(row=0,column=1,rowspan=2,sticky=W)
##        w = Label(self.fOpnames, text=" ",width="45")
##        w.grid(row=0,column=2,sticky=W)

        self.btnOpnamesUpdate = Button(self.fOpnames, text="Opnamegegevens bijwerken", command=self.fOpnamesUpdate,state=DISABLED)
        self.btnOpnamesUpdate.grid(row=0,column=2,sticky=NW,padx=5,pady=5)
        self.btnOpnamesCancel = Button(self.fOpnames, text="Gegevens terugzetten", command=self.fOpnamesCancel,state=DISABLED)
        self.btnOpnamesCancel.grid(row=1,column=2,sticky=NW,padx=5,pady=5)

    def hide(self):
        self.fToolbar.grid_forget()
        self.fAlbum.grid_forget()
        self.fDivide1.grid_forget()
        self.fDivide2.grid_forget()
        self.fDivide3.grid_forget()
        self.fTracks.grid_forget()
        self.fDivide4.grid_forget()
        self.fDivide5.grid_forget()
        self.fDivide6.grid_forget()
        self.fOpnames.grid_forget()

    def fAlbumUpdate(self):
        self.app.updatealbum(self.Type)
        self.fAlbum.grid_forget()
        self.fAlbum_show()

    def fAlbumCancel(self):
        self.fAlbum.grid_forget()
        self.fAlbum_show()

    def fTracksUpdate(self):
        self.app.updatetracks(self.Type)
        self.fTracks.grid_forget()
        self.fTracks_show()

    def fTracksCancel(self):
        self.fTracks.grid_forget()
        self.fTracks_show()

    def fOpnamesUpdate(self):
        self.app.updateopnames(self.Type)
        self.fOpnames.grid_forget()
        self.fOpnames_show()

    def fOpnamesCancel(self):
        self.fOpnames.grid_forget()
        self.fOpnames_show()

    def DettoStart(self):
        self.app.dettostart()
        
    def DettoSel(self):
        self.app.dettosel(self.Type)

    def DettoDetP(self):
        self.app.dettodet(self.Type,"PREV")
       
    def DettoDetN(self):
        self.app.dettodet(self.Type,"NEXT")

class Artiestenscherm:
    
    def __init__(self,app):
        self.app = app
        self.artId = IntVar()
        self.artNaam = StringVar()
        self.artSort = StringVar()
        self.master = app.master
        self.show()

    def show(self):
        tekst1 = "Lijst Uitvoerenden (met sortkey)"
        tekst2 = "Kies een artiest uit de lijst:"

        self.fToolbar = Frame(self.app.fKop)
        self.fToolbar.grid(row=0, column=2)
        self.btnBack = Button(self.fToolbar, text="Terug naar startscherm", command=self.ArttoStart)
        self.btnBack.grid(row=0,column=0,sticky=E)
        self.btnExit = Button(self.fToolbar, text="Exit", command=self.master.quit)
        self.btnExit.grid(row=0,column=1,sticky=E)

        fr = 4

        self.fTitle = Frame(self.master)
        self.fTitle.grid(row=fr, padx=5, pady=5)
        fr = fr + 1
        r = 0
        w = Label(self.fTitle, text=tekst1)
        w.grid(row=r,columnspan=3,sticky=W)

        self.fDivide1 = Frame(self.master, width=800, height=1)
        self.fDivide1.grid(row=fr,columnspan=3)
        fr = fr + 1
        self.fDivide2 = Frame(self.master, width=800, height=1, bg="#000000")
        self.fDivide2.grid(row=fr,columnspan=3)
        fr = fr + 1
        self.fDivide3 = Frame(self.master, width=800, height=1)
        self.fDivide3.grid(row=fr,columnspan=3)
        fr = fr + 1

        self.fSelect = Frame(self.master)
        self.fSelect.grid(row=fr, padx=5, pady=5)
        fr = fr + 1
        r = 0
        w = Label(self.fSelect, text=tekst2)
        w.grid(row=0,column=0,sticky=NW)
##        self.selectItem = Listbox(self.fSelect,height=20,width=60,bg="#ffffff",exportselection=0)
##        for item in self.app.vh.sellist:
##            self.selectItem.insert(END, item)
        self.selectItem = Pmw.ScrolledListBox(self.fSelect,
                items=self.app.artlist,
##                labelpos='nw',
##                label_text=tekst2,
                listbox_height = 20,
                listbox_width = 60,
                listbox_bg="#ffffff",
                selectioncommand=self.activateSelect,
##                dblclickcommand=self.defCmd,
##                usehullsize = 1,
##                hull_width = 200,
##                hull_height = 200,
        )
        self.selectItem.grid(row=0,column=1,rowspan=2,sticky=W)
        
        self.btnSelect = Button(self.fSelect, text="Wijzig gegevens", command=self.opendet,state=DISABLED)
        self.btnSelect.grid(row=0,column=2,sticky=NW, padx=5, pady=5)
        self.btnNew = Button(self.fSelect, text="Nieuwe artiest opvoeren", command=self.newdet)
        self.btnNew.grid(row=1,column=2,sticky=NW,padx=5)
        self.fr = fr

    def activateSelect(self):
        self.btnSelect.config(state=NORMAL)
        
    def hide(self):
        self.fToolbar.grid_forget()
        self.fTitle.grid_forget()
        self.fDivide1.grid_forget()
        self.fDivide2.grid_forget()
        self.fDivide3.grid_forget()
        self.fSelect.grid_forget()
        
    def opendet(self):
        # zoek het geselecteerde item in de listbox
        items = self.selectItem.curselection()
        try:
            items = map(int, items)
        except ValueError: pass
        if len(items) == 1:
            self.ix = items[0]
        # zoek de bijpassende entry 
        self.artId = self.app.ArtiestIds[self.ix]
        self.artNaam = self.app.ArtiestNamen[self.ix]
        self.artSort = self.app.ArtiestSkeys[self.ix]
        self.showdet()
        
    def newdet(self):
        self.artId = 0
        self.artNaam = ""
        self.artSort = ""
        self.showdet()

    def showdet(self):
        self.fDetail = Frame(self.master)
        self.fDetail.grid(row=self.fr, padx=5, pady=5)
        w = Label(self.fDetail, text="Artiest/groep:")
        w.grid(row=0, sticky=W)
        self.Titel = Entry(self.fDetail, width="60", textvariable=self.artNaam)
        self.Titel.delete(0,END)
        self.Titel.insert(END,self.artNaam)
        self.Titel.grid(row=0,column=1,columnspan=3,sticky=W)
        w = Label(self.fDetail, text="Sorteersleutel:")
        w.grid(row=1, sticky=W)
        self.Titel = Entry(self.fDetail, width="60", textvariable=self.artSort)
        self.Titel.delete(0,END)
        self.Titel.insert(END,self.artSort)
        self.Titel.grid(row=1,column=1,columnspan=3,sticky=W)
        self.btnUpdate = Button(self.fDetail, text="Wijzigen", command=self.wijzig)
        self.btnUpdate.grid(row=2,column=1, padx=5, pady=5)
        self.btnCancel = Button(self.fDetail, text="Afbreken", command=self.hidedet)
        self.btnCancel.grid(row=2,column=2, padx=5, pady=5)
        
    def wijzig(self):
        self.app.updateArtiest()
        
    def hidedet(self):
        self.fDetail.grid_forget()
        
    def ArttoStart(self):
        self.app.arttostart()

class Application:

    def __init__(self,master):
        self.selExists = 0
        self.detExists = 0
        self.artExists = 0
        self.artdetExists = 0
        self.which = ""
        self.what = ""
        self.how = ""
        # initialiseren gegevens vanuit de database
        ah = getArtiesten()
        self.ArtiestNamen = ah.ArtiestNamen
        self.ArtiestIds = ah.ArtiestIds
        self.ArtiestSkeys = ah.ArtiestSortkeys

        # initialiseren applicatiescherm
        self.master = Frame(master)
        self.master.grid(row=0,column=0)
        self.fKop = Frame(self.master)
        self.fKop.grid(row=0, sticky=W)
        w = Label(self.fKop, text="Magiokis Muziek!", font=("Verdana",18,"bold"), fg="#c00000")
        w.grid(row=0,sticky=W)
        w = Label(self.fKop, width=7, font=("Verdana",18,"bold"))
        w.grid(row=0,column=1,sticky=W)
        f = Frame(self.master, width=800, height=1)
        f.grid(row=1,columnspan=3)
        f = Frame(self.master, width=800, height=1, bg="#000000")
        f.grid(row=2,columnspan=3)
        f = Frame(self.master, width=800, height=1)
        f.grid(row=3,columnspan=3)

        # open startscherm
        self.start = Startscherm(self)

    def starttosel(self,type):
        # bepaal de selectie
##        master = item.master
        if type == "studio":
            whichitem = ["niks","artiest","titel","producer","credits","bezetting"]
            wh = self.start.selStudio.get() - 1
            self.which = whichitem[wh]
            if wh == 1:
                items = self.start.selectStudioArtist.curselection()
                try:
                    items = map(int, items)
                except ValueError: pass
                if len(items) == 1:
                    self.what = self.start.selectStudioArtist.get(items[0])
            elif wh != 1:
                self.what = self.start.txtStudio.get()
            items = self.start.selectStudioSort.curselection()
            try:
                items = map(int, items)
            except ValueError: pass
            if len(items) == 1:
                self.how = self.start.selectStudioSort.get(items[0])

        if type == "live":
            whichitem = ["niks","artiest","locatie","datum","bezetting"]
            wh = self.start.selLive.get() - 1
            self.which = whichitem[wh]
            if wh == 1:
                items = self.start.selectLiveArtist.curselection()
                try:
                    items = map(int, items)
                except ValueError: pass
                if len(items) == 1:
                    self.what = self.start.selectLiveArtist.get(items[0])
            elif wh != 1:
                self.what = self.start.txtLive.get()
            items = self.start.selectLiveSort.curselection()
            try:
                items = map(int, items)
            except ValueError: pass
            if len(items) == 1:
                self.how = self.start.selectLiveSort.get(items[0])

        if self.how == "Uitvoerende":
            self.how = "artiest"
        elif self.how == "Niets":
            self.how = ""
        else:
            self.how = self.how.lower()

        # haal de gegevens voor het nieuwe scherm op
        self.vh = getSelection(type,self.which,self.what,self.how)
        if len(self.vh.sellist) == 0:
            f = ('Geen %s albums gevonden' % type)
            if self.which != "niks":
                f = ('Geen %s albums gevonden met "%s" in "%s"' % (type, self.what, self.which))
            # fout melden op het huidige scherm
            tkMessageBox.showinfo("Helaas!",f)
            return

        # sluit het vorige scherm
        self.start.hide()
        
        # open een nieuw scherm
        if self.selExists:
            self.sel.show(type)
        else:
            self.selExists = 1
            self.sel = Selectiescherm(self,type)

    def starttodetail(self,type):
        "nieuw album opvoeren"
        # bepaal de op te halen gegevens
        self.dh = getDetail(type,0)
        self.ix = -1
        # sluit het vorige scherm
        self.start.hide()
        # open een nieuw scherm
#        self.start.show()
        if self.detExists:
            self.det.show(type)
        else:
            self.detExists = 1
            self.det = Detailscherm(self,type)

    def seltodetail(self,type,new=0):
        # bepaal de op te halen gegevens
        if new:
            self.dh = getDetail(type,0)
            self.ix = -1
            # basis voor de selectie al invullen
            self.dh.setProp(self.what,self.which)
        else:
            # zoek het geselecteerde item in de listbox
            items = self.sel.selectItem.curselection()
            try:
                items = map(int, items)
            except ValueError: pass
            if len(items) == 1:
                self.ix = items[0]
            # zoek de bijpassende entry in vh.keylist
            x = self.vh.keylist[self.ix]
            self.dh = getDetail(type,x)
        # sluit het vorige scherm
        self.sel.hide()
        # open een nieuw scherm
        # new geeft aan of er een nieuwe opgevoerd moet worden
        if self.detExists:
            self.det.show(type)
        else:
            self.detExists = 1
            self.det = Detailscherm(self,type)

    def seltostart(self):
        # sluit het vorige scherm
        self.sel.hide()
        # open een nieuw scherm
        self.start.show()

    def dettostart(self):
        # sluit het vorige scherm
        self.det.hide()
        # open een nieuw scherm
        self.start.show()

    def dettosel(self,type):
        # sluit het vorige scherm
        self.det.hide()
        # open een nieuw scherm
        self.sel.show(type)

    def dettodet(self,type,direction):
        # zoek de bijpassende entry in vh.keylist
        if direction == "PREV":
            if self.ix > 0:
                self.ix = self.ix - 1
        if direction == "NEXT":
            if self.ix < len(self.vh.keylist) - 1:
                self.ix = self.ix + 1
        x = self.vh.keylist[self.ix]
        self.dh = getDetail(type,x)
        # sluit het vorige scherm
        self.det.hide()
        # open een nieuw scherm
        self.det.show(type)

    def updatealbum(self,type):
        pass
        
    def updatetracks(self,type):
        pass
        
    def updateopnames(self,type):
        pass

    def starttoart(self):
        # haal de gegevens voor het nieuwe scherm op (is al gebeurd)
        self.artlist = []
        for ix in range(len(self.ArtiestNamen)):
            h = self.ArtiestNamen[ix] + " (" + self.ArtiestSkeys[ix] + ")"
            self.artlist.append(h)

        # sluit het vorige scherm
        self.start.hide()
        
        # open een nieuw scherm
        if self.artExists:
            self.art.show()
        else:
            self.artExists = 1
            self.art = Artiestenscherm(self)

    def arttostart(self):
        # sluit het vorige scherm
        self.art.hide()
        # open een nieuw scherm
        self.start.show()

    def updateArtiest(self):
        # haal de ingevulde gegevens op en werk ze bij
##        self.artNaam = self.art.artNaam.get()
##        self.artSort = self.art.artSort.get()
        adh = setArtiest(self.art.artId,self.art.artNaam,self.art.artSort)
    
##    def quit():
##        self.master.quit
        
        
root = Tk()
Pmw.initialise(root)

app = Application(root)

root.mainloop()

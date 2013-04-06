#! /usr/bin/env python

import cgi
import cgitb
cgitb.enable()
import muziek_ini
from meldfout import meldfout
from detail_main import Detail
from muziek_wijzig import Wijzig

def main():
    form = cgi.FieldStorage()
    form_ok = True
    foutregel = ''
    albumtype  = ''
    if "hStudio" in form or "hStudioN" in form:   # komt vanuit .. of startscherm
        albumtype = 'studio'
    elif "hLive" in form or "hLiveN" in form:   # komt vanuit .. of startscherm
        albumtype = 'live'
    if not albumtype:
        albumtype = form.getfirst("hTypeAlbum", '') # komt vanuit detailscherm bij wijzigen?
        if not albumtype:
            albumtype = form.getfirst("hType", '')   # komt mee vanuit selectiescherm
    wijzigO = form.getfirst("hWijzig", False)
    albumid = None
    if "hNieuw" in form:                      # komt vanuit startscherm
        # er valt nog niks aan te passen want er was nog niks ingevuld
        wijzigO = True
        dm = Detail(albumtype, wijzigO)
        albumid = dm.album_id
    if albumid is None:
        eerstWijzigen = False
        albumid = form.getfirst("selAlbum", None)
        if albumid is not None: # kwam mee vanuit selectiescherm (de oude)
            dm = Detail(albumtype, wijzigO, albumid)
            dm.set_arg("sZoek", form.getfirst("hSZoek"))
            dm.set_arg("tZoek", form.getfirst("hTZoek"))
            dm.set_arg("Sort", form.getfirst("hSort"))
    if albumid is None:
        albumid = form.getfirst("hId", None)
        if albumid is not None:  # komt mee vanuit selectiescherm (de nieuwe)
            dm = Detail(albumtype, wijzigO, albumid)
            dm.set_arg("sZoek", form.getfirst("hSZoek"))
            dm.set_arg("tZoek", form.getfirst("hTZoek"))
            dm.set_arg("Sort", form.getfirst("hSort"))
    if albumid is None:
        albumid = form.getfirst("hIdAlbum", None)
        if albumid is not None: # komt vanuit detailscherm bij wijzigen
            eerstWijzigen = True
            if form.getfirst("hWijzig", '') == "1":
                albumid = 0
            dm = Detail(albumtype, wijzigO, albumid)
            dm.set_arg("artiest", form.getfirst("selArtiest", None))
            dm.set_arg("titel", form.getfirst("txtTitel", None))
            dm.set_arg("label", form.getfirst("txtLabel", None))
            dm.set_arg("jaar", form.getfirst("txtJaar", None))
            dm.set_arg("producer", form.getfirst("txtProduced", None))
            dm.set_arg("credits", form.getfirst("txtCredits", None))
            dm.set_arg("bezetting", form.getfirst("txtBezetting", None))
            dm.set_arg("tracks", form.getfirst("listTracks", None))
            dm.set_arg("opnames", form.getfirst("listOpnames", None))
            h = dm.wijzig() # albumtype,albumid
    if albumid is None:
        foutregel = 'Geen albumid opgegeven'

    print "Content-Type: text/html"     # HTML is following
    print                               # blank line, end of headers
    if foutregel != '':
        meldfout(foutregel, "Magiokis Muziek!")
    else:
        dm.toon()
        for x in dm.regels:
            print x

if __name__ == '__main__':
	main()

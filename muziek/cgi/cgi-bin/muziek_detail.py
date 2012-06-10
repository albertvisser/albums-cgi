#! /usr/bin/env python

import cgi
import cgitb
cgitb.enable()
import muziek_ini
from meldfout import meldfout
from detail_main import Detail

def main():
    form = cgi.FieldStorage()
    form_ok = True
    foutregel = ''
    if "hStudio" in form or "hStudioN" in form:   # komt vanuit .. of startscherm
        albumtype = 'studio'
    elif "hLive" in form or "hLiveN" in form:   # komt vanuit .. of startscherm
        albumtype = 'live'
    else:
        albumtype = form.getfirst("hTypeAlbum", '') # komt vanuit detailscherm bij wijzigen
        if not albumtype:
            albumtype = form.getfirst("hType", '')  # komt mee vanuit selectiescherm
    wijzig = form.getfirst("hWijzig", 0)       # komt vanuit detailscherm
    albumid = None
    if "hNieuw" in form:                      # komt vanuit startscherm
        # er valt nog niks aan te passen want er was nog niks ingevuld
        dm = Detail(albumtype, wijzig=True)
        albumid = dm.album_id
    eerst_wijzigen = False
    albumid = form.getfirst("selAlbum", None)
    if not albumid:
        albumid = form.getfirst("hId", None)
    if not albumid:
        albumid = form.getfirst("hIdAlbum", None)
        eerst_wijzigen = True
    if not albumid:
        foutregel = 'Geen albumid opgegeven'
    elif eerst_wijzigen:
        if form.getfirst("hWijzig", None) == "1":
            albumid = 0
        dm = Detail(albumtype, wijzig, albumid)
        dm.artiest = form.getfirst("selArtiest", None)
        dm.titel = form.getfirst("txtTitel", None)
        dm.label = form.getfirst("txtLabel", None)
        dm.jaar = form.getfirst("txtJaar", None)
        dm.producer = form.getfirst("txtProduced", None)
        dm.credits = form.getfirst("txtCredits", None)
        dm.bezetting = form.getfirst("txtBezetting", None)
        dm.tracks = form.getfirst("listTracks", None)
        dm.opnames = form.getfirst("listOpnames", None)
        h = dm.wijzig() # albumtype,albumid
    else:
        dm = Detail(albumtype, wijzig, albumid)
        dm.zoeksoort = form.getfirst("hSZoek", None)
        dm.zoektekst = form.getfirst("hTZoek", None)
        dm.sortering = form.getfirst("hSort", None)
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

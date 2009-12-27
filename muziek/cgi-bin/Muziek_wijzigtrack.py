#~ vanuit detailscherm:
    #~ txtTitel bevat samengestelde waarde artiest/titel/label/jaar
    #~ hAlbumId
    #~ hAlbumType
    #~ hTrackId
    #~ txtTrack

import cgi
import muziek_ini
from meldfout import meldfout
from muziek_detail_main import detail_main
from muziek_wijzig import wijzig

def main():
    form = cgi.FieldStorage()
    form_ok = True
    #~ print "Content-Type: text/html"     # HTML is following
    #~ print                               # blank line, end of headers
    #~ print "<html>"
    #~ print "<head></head>"
    #~ print "<body>"
    #~ keys = form.keys()
    #~ keys.sort()
    #~ print
    #~ print "<H3>Form Contents:</H3>"
    #~ if not keys:
        #~ print "<P>No form fields."
    #~ print "<DL>"
    #~ for key in keys:
        #~ print "<DT>" + cgi.escape(key) + ":",
        #~ value = form[key]
        #~ print "<i>" + cgi.escape(`type(value)`) + "</i>"
        #~ print "<DD>" + cgi.escape(`value`)
    #~ print "</DL>"
    #~ print
    #~ print "</body></html>"
    #~ return
#--
#   initialisatie
    foutregel = ''
    if form.has_key("hStudio") or form.has_key("hStudioN"):   # komt vanuit .. of startscherm
        albumtype = 'studio'
    elif form.has_key("hLive") or form.has_key("hLiveN"):   # komt vanuit .. of startscherm
        albumtype = 'live'
    elif form.has_key("hTypeAlbum"): # komt vanuit detailscherm bij wijzigen
        albumtype = form["hTypeAlbum"].value
    elif form.has_key("hType"):                    # komt mee vanuit selectiescherm
        albumtype = form["hType"].value
    else:
        albumtype  = ''
    if form.has_key("wijzigO"):       # komt vanuit detailscherm
        wijzigO = form["hWijzig"].value
    else:
        wijzigO = 0
    if form.has_key("hNieuw"):                      # komt vanuit startscherm
        # er valt nog niks aan te passen want er was nog niks ingevuld
        wijzigO = True
        dm = detail_main(albumtype,wijzigO)
        albumid = dm.Id
    else:
        eerstWijzigen = False
        if form.has_key("selAlbum"): # kwam mee vanuit selectiescherm (de oude)
            albumid = form["selAlbum"].value
            dm = detail_main(albumtype,wijzigO,albumid)
            dm.setAttr("sZoek",form["hSZoek"].value)
            dm.setAttr("tZoek",form["hTZoek"].value)
            dm.setAttr("Sort",form["hSort"].value)
        elif form.has_key("hId"):                          # komt mee vanuit selectiescherm (de nieuwe)
            albumid = form["hId"].value
            dm = detail_main(albumtype,wijzigO,albumid)
            dm.setAttr("sZoek",form["hSZoek"].value)
            dm.setAttr("tZoek",form["hTZoek"].value)
            dm.setAttr("Sort",form["hSort"].value)
        elif form.has_key("hIdAlbum"): # komt vanuit detailscherm bij wijzigen
            eerstWijzigen = True
            if form["hWijzig"].value == "1":
                albumid = 0
            else:
                albumid = form["hIdAlbum"].value
            dm = detail_main(albumtype,wijzigO,albumid)
            if form.has_key("selArtiest"):
                dm.setAttr("artiest",form["selArtiest"].value)
            if form.has_key("txtTitel"):
                dm.setAttr("titel",form["txtTitel"].value)
            if form.has_key("txtLabel"):
                dm.setAttr("label",form["txtLabel"].value)
            if form.has_key("txtJaar"):
                dm.setAttr("jaar",form["txtJaar"].value)
            if form.has_key("txtProduced"):
                dm.setAttr("producer",form["txtProduced"].value)
            if form.has_key("txtCredits"):
                dm.setAttr("credits",form["txtCredits"].value)
            if form.has_key("txtBezetting"):
                dm.setAttr("bezetting",form["txtBezetting"].value)
            if form.has_key("listTracks"):
                dm.setAttr("tracks",form["listTracks"].value)
            if form.has_key("listOpnames"):
                dm.setAttr("opnames",form["listOpnames"].value)
            h = dm.wijzig() # albumtype,albumid
        else:
            albumid = ''
            foutregel = 'Geen albumid opgegeven'

    print "Content-Type: text/html"     # HTML is following
    print                               # blank line, end of headers
    if foutregel != '':
        meldfout(foutregel,"Magiokis Muziek!")
    else:
        dm.toon()
        for x in dm.regels:
            print x

if __name__ == '__main__':
	main()

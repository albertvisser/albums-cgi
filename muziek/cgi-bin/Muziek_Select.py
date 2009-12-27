import cgi
import muziek_ini
from muziek_select_main import select_main

def main():
    form = cgi.FieldStorage()
    form_ok = 0
    h =  select_main()
    if form.has_key("hStudio"):
        h.setArg('albumtype','studio')
        if form.has_key("selZoekS") and form["selZoekS"].value != 'None':
            sZoek = form["selZoekS"].value
            if sZoek == "artiest":
                h.setArg('tZoek',form["selArtiest"].value)
            else:
                h.setArg('tZoek',form["txtZoekS"].value)
            h.setArg('sZoek',sZoek)
        if form.has_key("selSortS"):
            h.setArg('sorteren',form["selSortS"].value)
    elif form.has_key("hLive"):
        h.setArg('albumtype','live')
        if form.has_key("selZoekL") and form["selZoekL"].value != 'None':
            sZoek = form["selZoekL"].value
            if sZoek == "artiest":
                h.setArg('tZoek',form["selArtiest"].value)
            else:
                h.setArg('tZoek',form["txtZoekL"].value)
            h.setArg('sZoek',sZoek)
        if form.has_key("selSortL"):
            h.setArg('sorteren',form["selSortL"].value)
    #-- toevoeging o.b.v. selector andere artiest op selectiescherm
    elif form.has_key("selArtiest"):
        h.setArg('albumtype',form["hType"].value)
        h.setArg('sZoek',form["hZoek"].value)
        h.setArg('tZoek',form["selArtiest"].value)
        h.setArg('sorteren',form["hSort"].value)
    #-- einde toevoeging
    elif form.has_key("hType"):
        h.setArg('albumtype',form["hType"].value)
        h.setArg('sZoek',form["hSZoek"].value)
        h.setArg('tZoek',form["hTZoek"].value)
        h.setArg('sorteren',form["hSort"].value)
    h.go()
    print "Content-Type: text/html"     # HTML is following
    for x in h.regels:
        print x

if __name__ == '__main__':
	main()

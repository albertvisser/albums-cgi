Files in this directory
=======================

.hgignore
    things not to be tracked
favicon.ico
    site icon
files.rst
    dit geval

cgi-bin/
........
    meldfout.py
        routine om scherm met foutmelding op te bouwen
            met mogelijkheid css en header mee te geven
    muziek_artiesten.py
        gebruikt cgi
        importeert muziek_ini; Artiesten, Fout uit muziek_artiesten
        doel: opbouwen toon- of edit scherm artiesten
        leest form keys "hNieuw", "edit" en "after"
        roept class Artiesten aan met args "editEntry", "selId", "afterId"
            en "sSort"
    muziek_detail.py
        gebruikt cgi
        importeert muziek_ini; Detail uit muziek_detail
        leest form keys
        doel: opbouwen detailscherm of aanroepen opvoeren/wijzigen routine
        roept class Detail aan, eerst indien nodig voor wijzigen en altijd voor
            scherm tonen
    muziek_ini.py
        globals, m.n. plaats waar de programmatuur staat
    muziek_select.py
        gebruikt cgi
        importeert muziek_ini; Select uit select_main
        doel: opbouwen selectiescherm
        roept class Select aan voor initialisatie
        leest form keys voor bepalen parameters
        roept methode go aan voor ophalen paginasource
    muziek_start.py
        gebruikt cgi
        importeert muziek_ini; start uit start_main
        doel: opbouwen startscherm
        roept start aan voor ophalen paginasource
    muziek_wijzigopname.py
        gebruikt cgi
        importeert muziek_ini; Detail uit muziek_detail
        doel: wijzigen opnamegegevens
        roept class Detail aan, eerst voor wijzigen en daarna voor scherm tonen
    muziek_wijzigtrack.py
        gebruikt cgi
        importeert muziek_ini; Detail uit muziek_detail
        doel: wijzigen trackgegevens
        roept class Detail aan, eerst voor wijzigen en daarna voor scherm tonen


dml/
....
    data manipulatie routines, aangeroepen door verwerkingsroutines

    _globals.py
        o.a. pad naar de data
    artiest.py
        definieert functie artiestenlijst en class Artiest voor data handling
        gebruikt xml.sax
        importeert _globals
    live.py
        definieert functie concertlist en class Concert voor data handling
        gebruikt xml.sax
        importeert _globals; artiestenlijst en Artiest uit artiest
    studio.py
        definieert functie albumlist en class Album voor data handling
        gebruikt xml.sax
        importeert _globals; artiestenlijst en Artiest uit artiest

dml/dtd/
........
    beschrijvingen hoe de data eruit moet zien

    live.dtd
    studio.dtd

html/
.....
    artiesten.html
        lijst artiesten
    detail.html
        detailscherm album
    detail_live.html
        detailscherm concert
    favicon.ico
        site icon
    index.html
        opstarten startscherm
    muziek.css
        styling info
    muziek.png
        preview startscherm voor op index
    select.html
        selectiescherm
    start.html
        startscherm

main_logic/
...........
    verwerkingsroutines, aangeroepen vanuit cgi responses
    deze vullen de html sources verder in aan de hand van de opgehaalde gegevens

    artiesten_main.py
        opbouwen artiestenscherm en wijzigen artiest
        gebruikt artiesten.html
        importeert globals
            artiestenlijst, Artiest uit dml/artiest
    detail_main.py
        opbouwen detailscherm en wijzigen album/concert
        gebruikt detail.html, detail_live.html
        importeert globals
            Artiest uit dml/artiest
            Album, albumlist uit dml/studio
            Concert, concertlist uit dml/live
    globals.py
        o.a. pad naar data, opbouwen schermkop
    select_main.py
        opbouwen selectiescherm
        gebruikt select.html
        importeert globals
            artiestenlijst, Artiest uit dml/artiest
            albumlist uit dml/studio
            concertlist uit dml/live
    start_main.py
        opbouwen startscherm
        gebruikt start.html
        importeert globals
            artiestenlijst uit dml/artiest


gui/
....
    gui frontend voor hetzelfde backend als de cgi versie
    voortgezet (althans begonnen) als projects/album_gui maar dan met QtWebkit

    muziek_schermen.py
        definieert classes: Startscherm, Selectiescherm, Detailscherm,
            Artiestenscherm, Application
        gebruikt Tkinter/pmw
        importeert muziek_verwerk
    muziek_verwerk.py
        definieert functies: lees_artiesten, update_artiest, sort_albums,
            sort_concerten, selection
        definieert class: Detail
        importeert albumlist, Album uit dml/studio
            concertlist, Concert uit dml/live
            Artiest, artiestenlijst uit dml/artiest

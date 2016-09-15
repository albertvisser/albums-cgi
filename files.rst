Files in this directory
=======================

main site
---------

    favicon.ico
        site icon
    index.html
        startpagina
    files.rst
        dit geval

adressen app
------------

adressen\cgi-bin\
.................
    cgi response routines

    adres_select.py
        opbouwen selectiescherm voor "school"
        gebruikt cgi
        importeert adr_padspecs; select uit adres_select_main
    adres_select_ans.py
        opbouwen selectiescherm voor "ans"
        gebruikt cgi
        importeert adr_padspecs; select uit adres_select_main
    adres_wijzig.py
        wijzigen "school" adres, linkt door naar adres_select.py
        gebruikt cgi
        importeert adr_padspecs, meldfout
            wijzig en adres uit adres_wijzig_main
    adres_wijzig_ans.py
        wijzigen "ans" adres, linkt door naar adres_select_ans.py
        gebruikt cgi
        importeert adr_padspecs, meldfout
            wijzig en adres uit adres_wijzig_main
    adr_padspecs.py
        o.a. pad naar de programmatuur
    meldfout.py
        routine om tekst met melding aan te maken

adressen\dml\
.............
    data manipulatie routines, aangeroepen door verwerkingsroutines

    adressen.py
        definieert classes NawList en Naw voor data handling
        gebruikt xml.sax

adressen\html\
..............
    html sources e.d.

    adressen.css
        styling
    favicon.ico
        site icon
    index.htm
        opstarten startscherm
    select.htm
        selectiescherm
    start.htm
        startscherm

adressen\main_logic\
....................
    verwerkingsroutines, aangeroepen vanuit cgi responses
    deze vullen de html sources verder in
    aan de hand van de opgehaalde gegevens

    adres_globals.py
        pad naar de data, diverse instellingen en variabelen
    adres_select_main.py
        opbouwen selectiescherm
        gebruikt select.htm
        importeert adres_globals; NawList uit adressen
    adres_wijzig_main.py
        wijzigen adres
        importeert adres_globals; Naw uit adressen

films app
---------

films\cgi-bin\
..............
    cgi response routines

    films_detail.py
        opbouwen detailscherm
        gebruikt cgi
        importeert films_padspecs, meld_fout
            detail_main uit films_detail_main
    films_padspecs.py
        o.a. pad naar programmatuur
    films_select.py
        opbouwen selectiescherm
        gebruikt cgi
        importeert films_padspecs
            select_main uit films_select_main

films\dml\
..........
    data manipulatie routines, aangeroepen door verwerkingsroutines

    Films.py
        definieert classes FilmlList en Film voor data handling
        gebruikt xml.sax
        importeert globals
    globals.py
        pad naar de data

films\html\
...........
    html sources e.d.

    detail.html
        detailscherm
    favicon.ico
        site icon
    films.css
        styling
    index.html
        startscherm
    select.html
        selectiescherm

films\main_logic\
.................
    verwerkingsroutines, aangeroepen vanuit cgi responses
    deze vullen de html sources verder in
    aan de hand van de opgehaalde gegevens

    films_detail_main.py
        opbouwen detailscherm
        gebruikt detail.html
        importeert films_globals, meld_fout
            Film uit Films
    films_globals.py
        o.a. pad naar de data
    films_select_main.py
        opbouwen selectiescherm
        gebruikt select.html
        importeert films_globals, meld_fout
            Filmlist uit films
    meld_fout.py
        routine om een foutmelding op te bouwen, evt css en header meegeven

muziek app
----------

muziek\cgi\cgi-bin\
...................
    cgi response routines

    meldfout.py
        routine om scherm met foutmelding op te bouwen
            met mogelijkheid css en header mee te geven
    meld_fout.py
        idem
    muziek_artiesten.py
        opbouwen toon- of edit scherm artiesten:
        leest form keys "hNieuw", "edit" en "after"
        roept artiesten_main aan met args "editEntry", "selId", "afterId"
            en "sSort"
        gebruikt cgi
        importeert muziek_ini; muziek_artiesten_main
    muziek_artiesten2.py
        aanpassen artiest en opbouwen toonscherm ter bevestiging
        leest form keys "hId", "tNaam", "tstraat" en "tsort"
        zet deze om in "selId", "hNaam", "hSort"
        roept artiest_wijzig aan en daarna artiesten_main
        gebruikt cgi
        importeert muziek_ini; muziek_artiesten_main
    Muziek_Detail.py
        opbouwen detailscherm of aanroepen opvoeren/wijzigen routine
            dit is (nog) detail_main.wijzig()
        gebruikt cgi
        importeert muziek_ini
            detail_main uit muziek_detail_main
            wijzig uit muziek_wijzig
    muziek_ini.py
        o.a. plaats waar de programmatuur staat
    Muziek_Select.py
        opbouwen selectiescherm
        gebruikt cgi
        importeert muziek_ini
            select_main uit muziek_select_main
    Muziek_Start.py
        opbouwen startscherm
        gebruikt cgi
        importeert muziek_ini
            start_main uit muziek_start_main
    Muziek_wijzigtrack.py
        kopie van muziek_detail om aan te passen voor het wijzigen van
            track informatie
        gebruikt cgi
        importeert muziek_ini
            meldfout uit meldfout
            detail_main uit muziek_detail_main
            wijzig uit muziek_wijzig

muziek\cgi\dml\
...............
    data manipulatie routines, aangeroepen door verwerkingsroutines

    globals.py
        o.a. pad naar de data
    muziek_artiest.py
        definieert classes ArtiestenLijst, Artiest voor data handling
        gebruikt xml.sax
        importeert globals
    muziek_live_met.py
        definieert classes ConcertList, Concert voor data handling
        gebruikt xml.sax
        importeert globals; ArtiestenLijst, Artiest uit muziek_artiest
    muziek_studio_met.py
        definieert classes AlbumList, Album voor data handling
        gebruikt xml.sax
        importeert globals; ArtiestenLijst, Artiest uit muziek_artiest
    muziek_studio_query.py
        uitprobeersel speciale query op Albums (minder nodig dan voor de
            versie in muziek_studio_met)?
        definieert class AlbumList
        gebruikt xml.sax
        importeert globals; ArtiestenLijst, Artiest uit muziek_artiest

muziek\cgi\dml\dtd\
...................
    beschrijvingen hoe de data eruit moet zien

    live.dtd
    studio.dtd

muziek\cgi\html\
................
    html sources e.d.

    artiesten.html
        lijst artiesten
        linkt voor wijzigen naar muziek_artiesten2.html
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
    Select.html
        selectiescherm
    Start.html
        startscherm

muziek\cgi\main_logic\
......................
    verwerkingsroutines, aangeroepen vanuit cgi responses
    deze vullen de html sources verder in
    aan de hand van de opgehaalde gegevens

    muziek_artiesten_main.py
        opbouwen artiestenscherm en wijzigen artiest
        gebruikt artiesten.html
        importeert muziek_globals
            Artiestenlijst, Artiest uit muziek_artiest
    muziek_detail_main.py
        opbouwen detailscherm en wijzigen album/concert
        gebruikt detail.html, detail_live.html
        importeert muziek_globals
            Artiest uit muziek_artiest
            Album, AlbumList uit muziek_studio_met
            Concert, ConcertList uit muziek_live_met
    muziek_globals.py
        o.a. pad naar data, opbouwen schermkop
    muziek_select_main.py
        opbouwen selectiescherm
        gebruikt select.html
        importeert muziek_globals
            Artiestenlijst, Artiest uit muziek_artiest
            AlbumList uit muziek_studio_met
            ConcertList uit muziek_live_met
    muziek_start_main.py
        opbouwen startscherm
        gebruikt start.html
        importeert muziek_globals
            Artiestenlijst uit muziek_artiest
    muziek_wijzig.py
        wijzigen album/concert
        code zit grotendeels ook in muziek_detail_main
            daar in class detail_main methode wijzig()
            hier in class wijzig() subclass van item()
        ik denk dat deze nog ten onrechte in muziek_detail.py hangt
        importeert
            Album uit muziek_studio_met
            Concert uit muziek_live_met

muziek\gui\
...........
    gui frontend voor hetzelfde backend als de cgi versie
    voortgezet (althans begonnen) als projects/album_gui maar dan met QtWebkit

    Muziek_schermen.py
        classes: Startscherm, Selectiescherm, Detailscherm, artiestenscherm,
            Application
        gebruikt Tkinter/pmw
        importeert getArtiesten, setArtiest, getSelection, getDetail
            uit Muziek_verwerk
    Muziek_verwerk.py
        classes: getArtiesten, getSelection, getDetail, setArtiest
        importeert AlbumList, Album uit muziek_studio_met
            ConcertList, Concert uit muziek_live_met
            Artiest, ArtiestenLijst uit muziek_artiest

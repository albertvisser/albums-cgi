Files in this directory
=======================

adressen app
------------

adressen\cgi-bin\
.................
    cgi response routines
adres_select.py
adres_select_ans.py
adres_wijzig.py
adres_wijzig_ans.py
adr_padspecs.py
meldfout.py

adressen\dml\
.............
    data manipulatie routines, aangeroepen door verwerkingsroutines
adressen.py

adressen\html\
..............
    html sources e.d.
adressen.css
favicon.ico
index.htm
select.htm
start.htm
temp.html

adressen\main_logic\
....................
    verwerkingsroutines, aangeroepen vanuit cgi responses
    deze vullen de html sources verder in
    aan de hand van de opgehaalde gegevens
adres_globals.py
adres_select_main.py
adres_wijzig_main.py

films app
---------

films\cgi-bin\
..............
    cgi response routines
films_detail.py
films_padspecs.py
films_select.py

films\dml\
..........
    data manipulatie routines, aangeroepen door verwerkingsroutines
Films.py
globals.py

films\html\
...........
    html sources e.d.
detail.html
favicon.ico
films.css
index.html
select.html

films\main_logic\
.................
    verwerkingsroutines, aangeroepen vanuit cgi responses
    deze vullen de html sources verder in
    aan de hand van de opgehaalde gegevens
films_detail_main.py
films_globals.py
films_select_main.py
meld_fout.py

muziek app
----------

muziek\cgi-bin\
...............
    cgi response routines
meldfout.py
meld_fout.py
muziek_artiesten.py
muziek_artiesten2.py
Muziek_Detail.py
muziek_ini.py
Muziek_Select.py
Muziek_Start.py
Muziek_wijzigtrack.py

muziek\dml\
...........
    data manipulatie routines, aangeroepen door verwerkingsroutines
globals.py
live.dtd
muziek_artiest.py
muziek_globals.py
muziek_live_met.py
muziek_opnames.py
muziek_studio_met.py
muziek_studio_query.py
studio.dtd

muziek\gui\
...........
    gui versie
Muziek_schermen.py
Muziek_verwerk.py

muziek\html\
............
    html sources e.d.
artiesten.html
detail.html
detail_live.htm
detail_live.html
favicon.ico
index.html
muziek.css
muziek_detail.html
Select.htm
Select.html
Start.htm
Start.html

muziek\main_logic\
..................
    verwerkingsroutines, aangeroepen vanuit cgi responses
    deze vullen de html sources verder in
    aan de hand van de opgehaalde gegevens
muziek_artiesten.py
muziek_artiesten_main.py
muziek_detail_main.py
muziek_globals.py
muziek_select_main.py
muziek_start_main.py
muziek_wijzig.py

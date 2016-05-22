httppad = "http://muziek.lemoncurry.nl/"
cgipad = httppad + "cgi-bin/"
# xmlpad = "C:/phpdev/www/pythoneer/Muziek/"
cssfile = httppad + "muziek.css"
htmlpad = "../html/"
docroot = "../dml"
import sys
sys.path.append(docroot) # waar de eigenlijke programmatuur staat

koptekst = """\
  <div>
    <span class="left5 vet groot"><a name="begin">Magiokis Muziek!</a></span>
    <span class="right5">&nbsp;
"""
hometekst = """\
<input type="button" value="Terug naar startscherm" onclick="%s"/>"""
backtekst ="""\
<form class="regel" action="{}muziek_select.py" method="post">
  <input type="hidden" name="hType" value="{}"/>
  <input type="hidden" name="hSZoek" value="{}" />
  <input type="hidden" name="hTZoek" value="{}"/>
  <input type="hidden" name="hSort" value="{}"/>
  <input type="submit" value="Terug naar selectie" />
</form>
"""
endtekst = """\
    </span><br/><br/><hr/>
  </div>"""

def kop(scherm, typ="", sz="", tz="", sor=""):
    regels = [koptekst]
    if scherm != "start":
        hgoto = ("window.location='%smuziek_start.py'" % cgipad)
        regels.append(hometekst % hgoto)
    if scherm == "detail":
        regels.append(backtekst.format(cgipad, typ, sz, tz, sor))
    regels.append(endtekst)
    return regels

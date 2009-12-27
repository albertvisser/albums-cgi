import cgi
import sys
from adr_padspecs import *
sys.path.append(progpad) # waar de eigenlijke programmatuur staat
from adres_wijzig_main import wijzig
from adres_wijzig_main import adres
from meldfout import meldfout

def main():
    form = cgi.FieldStorage()
    form_ok = 1
    if form.has_key("hId"):
        hA = adres(form["hId"].value)
    else:
        form_ok = 0
    if form_ok and form.has_key("tnaam"):
        hA.setAttr("naam",form["tnaam"].value)
    if form_ok and form.has_key("tstraat"):
        hA.setAttr("straat",form["tstraat"].value)
    if form_ok and form.has_key("tpostcode"):
        hA.setAttr("postcode",form["tpostcode"].value)
    if form_ok and form.has_key("tplaats"):
        hA.setAttr("plaats",form["tplaats"].value)
    if form_ok and form.has_key("ttel"):
        hA.setAttr("telefoon",form["ttel"].value)
    if form_ok and form.has_key("tgeboren"):
        hA.setAttr("geboren",form["tgeboren"].value)
    if form_ok and form.has_key("temail"):
        hA.setAttr("email",form["temail"].value)
    if not form_ok:
        m = "Alle rubrieken moeten worden ingevuld"
        h =  "Fout in invoer"
        s = httppad + "adressen.css"
        meldfout(m,h,s)
        return
    ln = wijzig("ans",hA)
    if ln.ok:
        print "Content-Type: text/html"     # HTML is following
        # doorlinken naar selectiescherm
        print ('Location: %sadres_select_ans.py' % cgipad)
    else:
        print "Content-Type: text/html"     # HTML is following
        print
        print "Wijzigen is niet gelukt"

if __name__ == '__main__':
    main()


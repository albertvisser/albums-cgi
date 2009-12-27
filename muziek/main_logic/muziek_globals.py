docroot= "F:/pythoneer/muziek/data"
httppad = "http://muziek.pythoneer.nl/"
cgipad = httppad + "cgi-bin/"
# xmlpad = "C:/phpdev/www/pythoneer/Muziek/"
cssfile = "http://muziek.pythoneer.nl/muziek.css"
htmlpad ="F:/www/pythoneer/muziek/"
import sys
sys.path.append(docroot) # waar de eigenlijke programmatuur staat
class kop:
    def __init__(self,scherm,typ="",sz="",tz="",sor=""):
        self.regels = ['  <div><span class="left5 vet groot"><a name="begin">Magiokis Muziek!</a></span><span class="right5">&nbsp;']
        if scherm != "start":
            hgoto = ("window.location='%smuziek_start.py'" % cgipad)
            self.regels.append('<input type="button" value="Terug naar startscherm" onclick="%s"/>' % hgoto)
        if scherm == "detail":
            self.regels.append('<form class="regel" action="%sMuziek_Select.py" method="post">'% cgipad)
            self.regels.append('  <input type="hidden" name="hType" value="%s"/>' % typ)
            self.regels.append('  <input type="hidden" name="hSZoek" value="%s" />' % sz)
            self.regels.append('  <input type="hidden" name="hTZoek" value="%s"/>' % tz)
            self.regels.append('  <input type="hidden" name="hSort" value="%s"/>' % sor)
            self.regels.append('  <input type="submit" value="Terug naar selectie" />')
            self.regels.append('</form>')
        self.regels.append('</span><br/><br/><hr/></div>')


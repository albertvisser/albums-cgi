xmlpad = "../data/" # was "f:/pythoneer/adressen/data/"
import sys
sys.path.append(xmlpad[:-1]) # voor de dml-functies
htmlpad = "../html/" # was "f:/www/pythoneer/adressen/"
httproot = "http:/adr.lemoncurry.nl" # was "http://adr.pythoneer.nl/"
cssfile = httproot + "adressen.css"
cgipad = httproot + "cgi-bin/"
school_xmldoc = xmlpad + "Adressen_school.xml"
school_select = cgipad + "adres_select.py"
school_wijzig = cgipad + "adres_wijzig.py"
school_velden = ('naam','straat','postcode','plaats','telefoon','email','geboren')
school_cols = (("30%","Naam"),("30%","Adres"),("20%","Telefoon/Email"),
               ("10%","Geboortedatum"))
school_inputs = ((("tnaam",""),),
                 (("tstraat","","<br />"),("tpostcode","8",""),("tplaats","")),
                 (("ttel","10","<br />"),("temail","20","")),
                 (("tdag","2","-"),("tmaand","2","-"),("tjaar","4")))
school_fields = ((1),(2,3,4),(5,6),((7,6,8),(7,4,6),(7,0,4)))
ans_xmldoc = xmlpad + "Adressen_ans.xml"
ans_select = cgipad + "adres_select_ans.py"
ans_wijzig = cgipad + "adres_wijzig_ans.py"
ans_velden = ('naam','straat','postcode','plaats','telefoon','email','geboren')
ans_cols = (("25%","Naam"),("30%","Adres"),("20%","Telefoon/Email"),
            ("15%","Geboren"))
ans_inputs = ((("tnaam",""),),
              (("tstraat","","<br />"),("tpostcode","8",""),("tplaats","")),
              (("ttel","10","<br />"),("temail","20","")),(("tdatum",""),))
ans_fields = ((1),(2,3,4),(5,6),(7))

htmlpad = "../html" # was "f:/www/pythoneer/adressen/"
httppad = "http://adr.lemoncurry.nl/" # was "http://adr.pythoneer.nl/"
cgipad = httppad + "cgi-bin/"
progpad = "../main_logic" # was "f:/pythoneer/adressen/"


# Gezocht naar 'htmlpad' in opgegeven bestanden/directories
# Gezocht naar 'httppad' in opgegeven bestanden/directories
# Gezocht naar 'cgipad' in opgegeven bestanden/directories
# Gezocht naar 'progpad' in opgegeven bestanden/directories
# De bestanden staan allemaal in of onder de directory "/home/albert/projects/pythoneer/adressen/cgi-bin/"
#
# adres_select_ans.py r. 4 sys.path.append(progpad) # waar de eigenlijke programmatuur staat
# adres_select_ans.py r. 17         f = file(htmlpad + "temp.html","w")
# adres_select.py r. 4 sys.path.append(progpad) # waar de eigenlijke programmatuur staat
# adres_select.py r. 17         f = file(htmlpad + "temp.html","w")
# adres_wijzig_ans.py r. 4 sys.path.append(progpad) # waar de eigenlijke programmatuur staat
# adres_wijzig_ans.py r. 33         s = httppad + "adressen.css"
# adres_wijzig_ans.py r. 40         print ('Location: %sadres_select_ans.py' % cgipad)
# adres_wijzig.py r. 4 sys.path.append(progpad) # waar de eigenlijke programmatuur staat
# adres_wijzig.py r. 42         s = httppad + "adressen.css"
# adres_wijzig.py r. 49         print ('Location: %sadres_select.py' % cgipad)

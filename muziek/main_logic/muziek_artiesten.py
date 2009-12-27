import cgi
import muziek_globals
cssfile = muziek_globals.cssfile
cgipad = muziek_globals.cgipad
##htmlpad = muziek_globals.htmlpad
from muziek_artiest import ArtiestenLijst

def main():
    form = cgi.FieldStorage()
    form_ok = 0
    sZoek = ''
    sSort = ''
    editEntry = 0
    selId = 0
    afterId = 0
    if form.has_key("hNieuw"):
        editEntry = 1
    if form.has_key("edit"):
        editEntry = 0
        selId = form["edit"].value
    if form.has_key("after"):
        editEntry = 0
        afterId = form["after"].value
        sSort = form["sort"].value
    lh = ArtiestenLijst()
    print "Content-Type: text/html"     # HTML is following
    print                               # blank line, end of headers
##    print "<br />editentry: " + str(editEntry)
##    print "<br />selid: "+ str(selId)
##    print "<br />afterid: "+ str(afterId)
##    return
    print '<?xml version="1.0" encoding="iso-8859-1"?>'
    print '<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN"'
    print '"http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">'
    print '<html xmlns="http://www.w3.org/1999/xhtml">'
    print '<head>'
    print '<meta http-equiv="Content-Type" content="text/html; charset=iso-8859-1" />'
    print ('  <link rel="stylesheet" href="%s" type="text/css" />' % cssfile)
    print '  <title>Adressen selectie</title>'
    print '</head>'
    print '<body>'
    print '  <table width="100%" border="1">'
    print '    <tr>'
    print '      <th width="45%">Naam</th>'
    print '      <th width="25%">Sorteerkey</th>'
    hgoto = ("javascript:document.location='%smuziek_artiesten.py?hNieuw=nieuw'" % cgipad)
    print '      <th width="30%"><input type="button" value="Nieuw" onclick="' + hgoto + '"></th>'
    print '    </tr>'
    for x in lh.Namen:
        if not editEntry:
            if x[0] == selId:
                editEntry = 1
            else:
                print '    <tr>'
                print ('      <td valign="top">%s</td>' % x[1])
                print ('      <td valign="top">%s</td>' % x[2])
                hgoto = ("javascript:document.location='%smuziek_artiesten.py?edit=%s'" % (cgipad,x[0]))
                hgoto2 = ("javascript:document.location='%smuziek_artiesten.py?after=%s&sort=%s'" % (cgipad,x[0],x[2]))
                print '      <td valign="top">'
                print ('        <input type="button" value="Wijzigen" onclick="%s">' % hgoto)
                print ('         <input type="button" value="Nieuw achtervoegen" onclick="%s">' % hgoto2)
                print '      </td>'
                print '    </tr>'
                if x[0] == afterId:
                    editEntry = 1
        if editEntry:
            editEntry = 0
            print '    <tr>'
            print ('    <form action="%smuziek_artiesten2.py" method="post">' % cgipad)
            if selId == 0:
                print '      <td valign="top"><input type="text" name="tnaam" id="tnaam" size="60" /></td>'
                print ('      <td valign="top"><input type="text" name="tsort" id="tsort" value="%s" /></td>' % sSort)
            elif x[0] == selId:
                print ('      <td valign="top"><input type="text" name="tnaam" id="tnaam" value="%s" size="60" /></td>' % x[1])
                print ('      <td valign="top"><input type="text" name="tsort" id="tsort" value="%s" /></td>' % x[2])
            print '      <td valign="top">'
            if selId == 0:
                print '        <input type="hidden" name="hId" id="hId" value="0" />'
            elif x[0] == selId:
                print ('       <input type="hidden" name="hId" id="hId" value="%s" />' % x[0])
            print '        <input type="submit" value="Aanpassen" />'
            print '        <input type="button" value="Terugzetten" onclick="javascript:history.go(-1)" />'
            print '      </td>'
            print '    </form>'
            print '    </tr>'

    print '  </table>'
    print '</body>'
    print '</html>'

if __name__ == '__main__':
    main()


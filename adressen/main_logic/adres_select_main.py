from adres_globals import *
from adressen import NawList
from types import *

def select(inp,editEntry,selId):
    if inp == "school":
        lh = NawList(school_xmldoc,school_velden)
        selprog = school_select
        wijzprog = school_wijzig
        cols = school_cols
        inputs = school_inputs
        fields = school_fields
    elif inp == "ans":
        lh = NawList(ans_xmldoc,ans_velden)
        selprog = ans_select
        wijzprog = ans_wijzig
        cols = ans_cols
        inputs = ans_inputs
        fields = ans_fields
    regels = []
    fh = open(htmlpad + "select.htm")
    for x in fh.readlines():
        y = x[:-1]
        if y.find("link rel") > 0:
            regels.append(y % cssfile)
        elif y.find('value="Nieuw"') > 0:
            hgoto = ("javascript:document.location='%s?edit=0'" % selprog)
            z = y.split("%s")
            regels.append(hgoto.join(z))
        elif y == "<!-- kopregel -->":
            for c in cols:
                regels.append('      <th width="%s">%s</th>' % (c[0],c[1]))
        elif y == "<!-- dataregel -->":
            if editEntry and selId == "0":
                editEntry = 0
                regels.append('    <tr>')
                regels.append('    <form action="%s" method="post">' % wijzprog)
                for z in inputs:
                    s = '      <td valign="top">'
                    for zz in z:
                        ss1 = ""
                        if zz[1] != "": ss1 = (' size="%s"' % zz[1])
                        ss2 = ""
                        if len(zz) == 3: ss2 = zz[2]
                        s = s + ('<input type="text" name="%s" id="%s"%s />%s' % (zz[0],zz[0],ss1,ss2))
                    s = s + '</td>'
                    regels.append(s)
                regels.append('      <td valign="top"><input type="hidden" name="hId" id="hId" value="0" /><input type="submit" value="Aanpassen" /><br /><input type="button" value="Terugzetten" onclick="javascript:history.go(-1)" /></td>')
                regels.append('    </form>')
                regels.append('    </tr>')
            for x in lh.Items:
                regels.append('    <tr>')
                if editEntry and x[0] == selId:
                    eerste = True
                    for c in cols:
                        if eerste:
                            s = '<a name="wijzigdeze"></a>'
                            eerste = False
                        else:
                            s = ''
                        regels.append('      <td>%s%s</td>' % (s,c[1]))
                    regels.append('      <td>&nbsp;</td>')
                    regels.append('    </tr>')
                    regels.append('    <tr>')
                    editEntry = 0
                    regels.append('    <form action="%s" method="post">' % wijzprog)
                    for i in range(len(inputs)):
                        s = '      <td valign="top">'
                        z = inputs[i]
                        r =  fields[i]
                        j = 0
                        for zz in z:
                            ss1 = ""
                            if zz[1] != "": ss1 = (' size="%s"' % zz[1])
                            ss2 = ""
                            if len(zz) == 3: ss2 = zz[2]
                            if type(r) is IntType:
                                w = x[r]
                            else:
                                if type(r[j]) is IntType:
                                    i0 = r[j]
                                    w = x[i0]
                                else:
                                    i0 = r[j][0]
                                    i1 = r[j][1]
                                    i2 = r[j][2]
                                    w = x[i0][i1:i2]
                                j = j + 1
                            s = s + ('<input type="text" name="%s" id="%s"%s value="%s"/>%s'
                                     % (zz[0],zz[0],ss1,w,ss2))
                        s = s + '</td>'
                        regels.append(s)
##                        regels.append(s % fields[i])
# school_fields = (x[1], (x[2],x[3],x[4]), x[5], (x[6][6:8],x[6][4:6],x[6][0:4]) )
# ans_fields = (x[1], (x[2],x[3],x[4]), x[5], x[6], x[7])
                    regels.append('      <td valign="top"><input type="hidden" name="hId" id="hId" value="%s" /><input type="submit" value="Aanpassen" /><br /><input type="button" value="Terugzetten" onclick="javascript:history.go(-1)" />' % x[0])
                    regels.append('    </form>')
                else:
                    if inp == "school":
                        regels.append('      <td valign="top">%s</td>' % x[1])
                        regels.append('      <td valign="top">%s<br />%s %s</td>' % (x[2],x[3],x[4]))
                        h = x[5]
                        hh = x[6]
                        if h == "": h = "&nbsp;"
                        if hh == "": hh = "&nbsp;"
                        regels.append('      <td valign="top">%s<br />%s</td>' % (h,hh))
                        h = x[7]
                        if h == "":
                            d = "&nbsp;"
                        else:
                            d = h[6:8] + "-" + h[4:6] + "-" + h[0:4]
                        regels.append('      <td valign="top">%s</td>' % d)
                    if inp == "ans":
                        regels.append('      <td valign="top">%s</td>' % x[1])
                        regels.append('      <td valign="top">%s<br />%s %s</td>' % (x[2],x[3],x[4]))
                        h = x[5]
                        if h == "": h = "&nbsp;"
                        hh = x[6]
                        if hh == "": hh = "&nbsp;"
                        regels.append('      <td valign="top">%s<br />%s</td>' % (h,hh))
                        h = x[7]
                        if h == "": h = "&nbsp;"
                        regels.append('      <td valign="top">%s</td>' % h)
                    hgoto = ("javascript:document.location='%s?edit=%s'" % (selprog,x[0]))
                    regels.append('      <td valign="top"><input type="button" value="Wijzigen" onclick="%s">' % hgoto)
                regels.append('    </tr>')
        elif x[:4] != "<!--" :
            regels.append(y)
    fh.close()
    return regels

if __name__ == '__main__':
    test = "ans"
    select(test,1,"")

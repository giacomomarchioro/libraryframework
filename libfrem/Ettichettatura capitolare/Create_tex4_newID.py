
import qrcode
import os

collocazione = "1.3.4"
fld = "Latex_soruce"
if not os.path.exists(fld):
    os.makedirs(fld)
fldQRc = os.path.join(fld,"QRcodes")
if not os.path.exists(fldQRc):
    os.makedirs(fldQRc)

selected = ["DCCXIX","DCCCLV","CCCCXLV","DCLIV","DCCCXVII",
"DCCCXVIII",
"DCCCXIX",]
with open('lista manoscritti - Versione_con_aggiunte.csv','r') as f, open('latex_temp2.tex','r') as template, open(os.path.join(fld,'labels.tex'),'w') as fl:
    for line in template:
        fl.write(line)
    next(f)
    for i in f:
        splitted = i.split(',')
        titolo = splitted[15].lower()
        if titolo == '':
            titolo = 'n.d.'
        idx = splitted[1]
        numerocodice = splitted[8]
        if numerocodice in selected:
            collocazione = splitted[5]
            #qrline = "%s # %s # %s # lv. 1 " %(idx,numerocodice,titolo)
            scalefactor = 2
            l_cod = len(numerocodice)
            if l_cod > 9:
                scalefactor= 1.5
            elif l_cod > 13:
                scalefactor = 1
            if len(titolo) > 16:
                rtitolo = titolo[:16]
                if len(titolo) > 60:
                    titolo = "".join([titolo[:60],r"\ldots"])
            else:
                rtitolo = titolo
            qrline = "".join([idx,(numerocodice+" ").rjust(18),rtitolo.rjust(16),"2"])
            print(qrline)
            img = qrcode.make(qrline)
            img.save(os.path.join(fldQRc,"%s.png"%idx))
            cmd = r"\booklabel{%s}{%s}{%s}{%s}{green}{%s}" %(idx,collocazione,numerocodice,titolo,scalefactor)
            fl.write(cmd+"\n")
    fl.write(r"\end{document}" + "\n")

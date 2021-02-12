import qrcode
import os

collocazione = "1.3.4"
fld = "Latex_soruce"
if not os.path.exists(fld):
    os.makedirs(fld)
fldQRc = os.path.join(fld,"QRcodes")
if not os.path.exists(fldQRc):
    os.makedirs(fldQRc)

with open('selezione.csv','r') as f, open('latex_temp.tex','r') as template, open(os.path.join(fld,'labels.tex'),'w') as fl:
    for line in template:
        fl.write(line)
    next(f)
    for i in f:
        splitted = i.split(';')
        titolo = splitted[13].lower()
        if titolo == '':
            titolo = 'n.d.'
        idx = splitted[0]
        numerocodice = splitted[6]
        collocazione = splitted[4]
        #qrline = "%s # %s # %s # lv. 1 " %(idx,numerocodice,titolo)
        if len(titolo) > 16:
            rtitolo = titolo[:16]
            if len(titolo) > 60:
                titolo = "".join([titolo[:60],r"\ldots"])
        else:
            rtitolo = titolo
        qrline = "".join([idx.zfill(5),(numerocodice+" ").rjust(18),rtitolo.rjust(16),"2"])
        print(qrline)
        img = qrcode.make(qrline)
        img.save(os.path.join(fldQRc,"%s.png"%idx))
        cmd = r"\booklabel{%s}{%s}{%s}{%s}{green}" %(idx,collocazione,numerocodice,titolo)
        fl.write(cmd+"\n")
    fl.write(r"\end{document}" + "\n")

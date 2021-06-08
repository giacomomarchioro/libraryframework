import os

os.listdir("converted")
# 
# exiftool -ext tif -tagsfromfile @ -srcfile %f.jp2 /Users/univr/Pictures/m0171_0/converted -XMP:format= -ImageHistory='Image technical metadata values were copied (via exiftool) from a source image to this derivative JP2 copy.' -overwrite_original
# prima cifra ID seconda ID da cui derivato
idx = 2
origine = 1
namelist = os.listdir(os.getcwd())
for g in namelist:
    if g.endswith('.tif'):
        nome,estensione = g.split('.')
        if origine is None:
            origine = nome[-2]
        new = "".join((nome[:-2],str(idx),str(origine),"."+estensione))
        os.rename(g,new)
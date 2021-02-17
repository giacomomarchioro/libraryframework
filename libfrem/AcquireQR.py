from tkinter.messagebox import RETRY
from pyzbar import pyzbar
import cv2
import time
import os 

if os.name == 'nt':
    import winsound
    def Beep():
        winsound.Beep(2500, 500)
        return True
else:
    def Beep():
        print('\007')
    #cv2.startWindowThread()


        

def acquireQR(autoreturn=False):
    vs = cv2.VideoCapture(0)
    lastread = 'No QR code found!'
    cv2.namedWindow("image")
    first = True
    while True:
        _, frame = vs.read()
        barcodes = pyzbar.decode(frame)
        for barcode in barcodes:
            (x, y, w, h) = barcode.rect
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)
            barcodeData = barcode.data.decode("utf-8")
            # barcodeType = barcode.type
            cv2.putText(frame, barcodeData, (x, y - 10),
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
            lastread = barcodeData
            if first:
                Beep()
                first = False
            if autoreturn:
                break
                
        
        cv2.putText(frame, lastread, (0,20),
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
        cv2.imshow("Avvicina il codice QR alla camera (premi spazio per terminare)", frame)
        k = cv2.waitKey(1) & 0xFF

        # if the `ESC` key was pressed, break from the loop
        if k%256 == 27:
            vs.release()
            cv2.destroyAllWindows()
            for i in range (1,5):
                cv2.waitKey(1)
            return False
        if k%256 == 32: # spacebar
            print("pressed sapcebar")
            break

    vs.release()
    cv2.destroyAllWindows()
    for i in range (1,5):
        cv2.waitKey(1)
    return lastread

def acquireQRandInfo(choices,frase, autoreturn=False,saveimage=False,filename=None):
    vs = cv2.VideoCapture(0)
    lastread = 'No QR code found!'
    id_dest = None
    destinazione = None
    motivazione = None
    status = "Aspetto gli input"
    first = True
    c = (0,0,255)
    while True:
        _, frame = vs.read()
        barcodes = pyzbar.decode(frame)
        for barcode in barcodes:
            (x, y, w, h) = barcode.rect
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)
            barcodeData = barcode.data.decode("utf-8")
            # barcodeType = barcode.type
            cv2.putText(frame, barcodeData, (x, y - 10),
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
            lastread = barcodeData
            if autoreturn:
                break
        
        if lastread != 'No QR code found!':
            c = (0,255,0)
            if first:
                Beep()
                first = False

        cv2.putText(frame, lastread, (0,20),
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, c, 2)
        if destinazione is None:
            y0, dy = 200, 15
            for i in choices:
                y = y0 + i*dy
                line = "%s - %s" %(i,choices[i])
                cv2.putText(frame, line, (300, y ), cv2.FONT_HERSHEY_SIMPLEX,0.5, (0,0,255), 2,)
            cv2.putText(frame,frase, (300,y0 - 15 ),
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,255), 2)
        if destinazione is not None:
            frase = "-> " + destinazione 
            cv2.putText(frame,frase, (300,y0 - 15),
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,255,0), 2,)
        
        

        cv2.imshow("Avvicina il codice QR alla camera (premi ESC per annluare SPAZIO per confermare le scelte)", frame)
        k = cv2.waitKey(1) & 0xFF
        # if the `ESC` key was pressed, break from the loop
        if (k%256 - 48) in choices.keys():
            id_dest = k%256 - 48
            destinazione = choices[id_dest]
        # if the `ESC` key was pressed, break from the loop
        if k%256 == 27:
            vs.release()
            cv2.destroyAllWindows()
            return False
        if k%256 == 32: # spacebar
            print("pressed sapcebar")
            if destinazione is not None and lastread != 'No QR code found!':
                if saveimage:
                    object_ID = int(lastread[:5])
                    print('salvo in %s' %(filename))
                    cv2.imwrite("%s_%s.jpeg"%(filename,object_ID), frame)
                    time.sleep(1)
                break

    vs.release()
    cv2.destroyAllWindows()
    for i in range (1,5):
        cv2.waitKey(1)
    return (lastread,destinazione)
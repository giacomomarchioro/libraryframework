from pyzbar import pyzbar
import cv2
import winsound
        

def acquireQR(autoreturn=False):
    vs = cv2.VideoCapture(0)
    lastread = 'No QR code found!'
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
        
        cv2.putText(frame, lastread, (0,20),
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
        cv2.imshow("Avvicina il codice QR alla camera (premi ESC per terminare)", frame)
        k = cv2.waitKey(1) & 0xFF
        # if the `ESC` key was pressed, break from the loop
        if k%256 == 27:
            break

    vs.release()
    cv2.destroyAllWindows()
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
                winsound.Beep(2500, 500)
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
            if destinazione is not None and lastread != 'No QR code found!':
                if saveimage:
                    campi = lastread.split(' # ')
                    object_ID = int(campi[0])
                    cv2.imwrite("%s_%s.jpeg" %(filename,object_ID), frame)
                break

    vs.release()
    cv2.destroyAllWindows()
    return (lastread,destinazione)
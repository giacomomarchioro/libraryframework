import cv2

cv2.namedWindow("preview")
vc = cv2.VideoCapture(0)
qrCodeDetector = cv2.QRCodeDetector()

if vc.isOpened(): # try to get the first frame
    rval, frame = vc.read()
else:
    rval = False

while rval:
    cv2.imshow("preview", frame)
    rval, frame = vc.read()
    key = cv2.waitKey(20)
    decodedText, points, _ = qrCodeDetector.detectAndDecode(frame)
    if points is not None:
 
        nrOfPoints = len(points)
 
        for i in range(nrOfPoints):
            nextPointIndex = (i+1) % nrOfPoints
            cv2.line(image, tuple(points[i][0]), tuple(points[nextPointIndex][0]), (255,0,0), 5)
 
            print(decodedText)  
    else:
        print("QR code not detected")

    if key == 27: # exit on ESC
        break

cv2.destroyWindow("preview")
vc.relase()
from pyzbar import pyzbar
import cv2

vs = cv2.VideoCapture(0)
lastread = 'No QR code found!'
while True:
	_, frame = vs.read()
	barcodes = pyzbar.decode(frame)
	for barcode in barcodes:
		(x, y, w, h) = barcode.rect
		cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)
		barcodeData = barcode.data.decode("utf-8")
		#barcodeType = barcode.type
		cv2.putText(frame, barcodeData, (x, y - 10),
			cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
		lastread = barcodeData
	
	cv2.putText(frame, lastread, (0,20),
			cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
	cv2.imshow("Avvicina il codice QR alla camera (premi 'a' per acquisire)", frame)
	key = cv2.waitKey(1) & 0xFF
	if key == ord("a"):
		break

vs.release()
cv2.destroyAllWindows()

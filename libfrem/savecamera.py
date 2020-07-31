import cv2


def acquirephoto(filename,instruction):
    cam = cv2.VideoCapture(0)
    img_counter = 0
    command = None
    while True:
        ret, frame = cam.read()
        cv2.imshow("%s press ESC to acquire the image" %(instruction), frame)
        if not ret:
            break
        k = cv2.waitKey(1) & 0xFF
        if k == ord("s"):
            print("Skipped")
            break  
        if k == ord("a"):
            cv2.imwrite(filename, frame)
            print("{} written!".format(filename))
            break    
        if k%256 == 27:
            # ESC pressed
            cv2.imwrite(filename, frame)
            print("{} written!".format(filename))
            command = 'esc'
            break
    cam.release()
    cv2.destroyAllWindows()
    return command 

def autoacquire(filename,ramping=5):
    cam = cv2.VideoCapture(0)
    img_counter = 0
    command = None
    for i in range(ramping):
        ret, frame = cam.read()
    cv2.imwrite(filename, frame)
    cam.release()
    cv2.destroyAllWindows()
    return command 
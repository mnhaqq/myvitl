import cv2
from pyzbar.pyzbar import decode
import time

def scan_code():
    cam = cv2.VideoCapture(0)
    cam.set(5, 640)
    cam.set(6, 480)

    camera = True
    ans = None

    while camera:
        ret, frame = cam.read()
        for code in decode(frame):
            ans = code.data.decode('utf-8')

            time.sleep(2)
            camera = False

        cv2.imshow('QR Code Scanner', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        
    cv2.destroyAllWindows()
    return ans

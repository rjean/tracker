#https://raspberrypi.stackexchange.com/questions/34318/pil-image-from-picamera-capture
import io
import time
import cv2

from rtcom import RealTimeCommunication
import pantilt

with RealTimeCommunication("turret.local") as rtcom:
    beat=0
    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_BUFFERSIZE,3)

    horizontal_angle=0
    vertical_angle=0

    while(True):
        ret, frame = cap.read()
        
        encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 70]
        ret, jpg_image = cv2.imencode("*.jpg",frame, encode_param)
        rtcom.broadcast_endpoint("jpeg_image", bytes(jpg_image), encoding="binary", addr="10.0.0.224")
        rtcom.broadcast_endpoint("heartbeat", beat)

        if "pc" in rtcom and "coordinates" in rtcom["pc"]:
            pantilt.set_horizontal_angle(rtcom["pc"]["coordinates"]["horizontal_angle"])
            pantilt.set_vertical_angle(rtcom["pc"]["coordinates"]["vertical_angle"])

        beat+=1
        time.sleep(0.020)

#https://raspberrypi.stackexchange.com/questions/34318/pil-image-from-picamera-capture
import io
import time
import cv2

from rtcom import RealTimeCommunication

with RealTimeCommunication("turret.local", listen=False) as rtcom:
    beat=0
    cap = cv2.VideoCapture(0)
    while(True):
        ret, frame = cap.read()
        encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 90]
        ret, jpg_image = cv2.imencode("*.jpg",frame, encode_param)
        rtcom.broadcast_endpoint("jpeg_image", bytes(jpg_image), encoding="binary")
        rtcom.broadcast_endpoint("heartbeat", beat)
        beat+=1
        time.sleep(0.1)

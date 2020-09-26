from rtcom import RealTimeCommunication
import cv2
import numpy as np
from time import sleep

with RealTimeCommunication("pc") as rtcom:
    horizontal_angle=0
    vertical_angle=0
    while True:
        try:
            if rtcom["turret.local"]["jpeg_image"] is not None:
                jpg_data = np.asarray(rtcom["turret.local"]["jpeg_image"])
                img = cv2.imdecode(jpg_data, cv2.IMREAD_UNCHANGED)
                cv2.imshow("preview", img) 
            key = cv2.waitKey(20)
            if key==-1: 
                key=None
            else:
                key=chr(key)

            if key=="c":
                horizontal_angle=0
                vertical_angle=0
            if key=="a":
                horizontal_angle-=1
            if key=="d":
                horizontal_angle+=1
            if key=="w":
                vertical_angle-=1
            if key=="s":
                vertical_angle+=1
            
            rtcom.broadcast_endpoint("coordinates",{"horizontal_angle" : horizontal_angle, 
                                                    "vertical_angle": vertical_angle })
            if key==27:
                break
        except KeyError:
            pass


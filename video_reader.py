from rtcom import RealTimeCommunication
import cv2
import numpy as np
from time import sleep

def write_header(image, text):
    cv2.putText(img,text, (10,30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 1)

def write_line(image, line_number, text):
    cv2.putText(image,text, (10,60+20*line_number), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,255), 1)
with RealTimeCommunication("pc") as rtcom:
    horizontal_angle=0
    vertical_angle=0
    while True:
        try:
            if rtcom["turret.local"]["jpeg_image"] is not None:
                jpg_data = np.asarray(rtcom["turret.local"]["jpeg_image"])
                img = cv2.imdecode(jpg_data, cv2.IMREAD_UNCHANGED)
                write_header(img, "Video Feed")
                perf = rtcom["turret.local"]["perf"]
                data = rtcom["turret.local"]["data"]
                for i, name in enumerate(perf):
                    write_line(img, i, f"{name} : {perf[name]*1000:0.1f}")

                for i, name in enumerate(data):
                    write_line(img, i+10, f"{name} : {data[name]:0.1f}")                
                
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


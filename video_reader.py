from rtcom import RealTimeCommunication
import cv2
import numpy as np

with RealTimeCommunication("pc") as rtcom:
    
    while True:
        try:
            jpg_data = np.asarray(rtcom["turret.local"]["jpeg_image"])
            img = cv2.imdecode(jpg_data, cv2.IMREAD_UNCHANGED)
            cv2.imshow("preview", img) 
            key = cv2.waitKey(20)
            if key==27:
                break
        except KeyError:
            pass


import io
import time
import cv2

from rtcom import RealTimeCommunication
import pantilt
from detect_image import make_interpreter, draw_objects, load_labels
import detect
from PIL import Image, ImageDraw
import numpy as np
from threading import Thread

import cv2, queue, threading, time

from utils import VideoCapture

def draw_and_broadcast(pil_frame, objs, labels, rtcom):
    draw_objects(ImageDraw.Draw(pil_frame), objs, labels)
    frame = np.array(pil_frame)
    frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
    
    encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 70]
    ret, jpg_image = cv2.imencode("*.jpg",frame, encode_param)

    rtcom.broadcast_endpoint("jpeg_image", bytes(jpg_image), encoding="binary", addr="10.0.0.224")

with RealTimeCommunication("turret.local") as rtcom:
    beat=0
    P = 0.05
    D = 0.05
    cap = VideoCapture(0)
    #cap.set(cv2.CAP_PROP_BUFFERSIZE,3)

    #cap.set(cv2.CAP_PROP_FRAME_WIDTH, 300)
    #cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 300)

    interpreter = make_interpreter("ssd_mobilenet_v2_coco_quant_postprocess_edgetpu.tflite")
    interpreter.allocate_tensors()

    #width, height = input_size(interpreter)

    horizontal_angle=0
    vertical_angle=0
    hysteresis = 10
    lost=0
    last_horizontal_error=0

    first_pass = True
    labels = load_labels("coco_labels.txt")
    perf = {} 
    data = {}
    loop_start_time=0



    while(True):
        data["Cycle Time"] = ((time.perf_counter() - loop_start_time)*1000, "ms")
        loop_start_time=time.perf_counter()
        start = time.perf_counter()
        frame = cap.read()
        data["Capture time"] = ((time.perf_counter() - loop_start_time)*1000, "ms")
        #print(f"Capture time: {time.perf_counter()-start}")
        start = time.perf_counter()
        
        pil_frame = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
        
        start = time.perf_counter()

        scale = detect.set_input(interpreter, pil_frame.size,
                           lambda size: pil_frame.resize(size, Image.NEAREST))

        
        
        #print(f"Scaling time: {time.perf_counter()-start}")
        data["Scaling time"] = ((time.perf_counter()-start)*1000, "ms")
        start = time.perf_counter()

        interpreter.invoke()
        objs = detect.get_output(interpreter, 0.4, scale)

        #print(f"Inference time: {}")
        data["Inference time"] = ((time.perf_counter()-start)*1000, "ms")
        start = time.perf_counter()

       # print(objs)
        
        center_v = 240
        center_h = 320


        max_score=0
        lost=lost+1
        for obj in objs:
            if obj.id== 0 and obj.score > 0.4:
                if obj.score > max_score:
                    center_h = (obj.bbox.xmax+obj.bbox.xmin)/2
                    center_v = (obj.bbox.ymax+obj.bbox.ymin)/2
                    max_score = obj.score
                    lost=0

        if lost > 10:
            horizontal_angle=0
            vertical_angle=0

        horizontal_error = (center_h-320)
        delta_horizontal_error = horizontal_error-last_horizontal_error
        last_horizontal_error=horizontal_error

        data["Horizontal error"] = (horizontal_error, "pixels")
        data["Horizontal angle"] = (horizontal_angle, "degrees")

        if abs(horizontal_error) > hysteresis:        
            horizontal_angle = horizontal_angle + P*horizontal_error + D*delta_horizontal_error

        #if True:
        #    draw_objects(ImageDraw.Draw(pil_frame), objs, labels)
        #    frame = np.array(pil_frame)
        #    frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
        thread = Thread(target = draw_and_broadcast, args = (pil_frame, objs, labels, rtcom))
        thread.start()

        data["Broadcast time"] = ((time.perf_counter()-start)*1000, "ms")
        start = time.perf_counter()
        #draw_and_broadcast(pil_frame, objs, labels, rtcom)
        #print(f"Draw time: {time.perf_counter()-start}")
        #data["Draw time"] = ((time.perf_counter()-start)*1000, "ms")
        #start = time.perf_counter()
        
        #encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 70]
        #ret, jpg_image = cv2.imencode("*.jpg",frame, encode_param)

        #print(f"Compress time: {time.perf_counter()-start}")
        #data["Compress time"] = ((time.perf_counter()-start)*1000, "ms")
        #start = time.perf_counter()

        #rtcom.broadcast_endpoint("jpeg_image", bytes(jpg_image), encoding="binary", addr="10.0.0.224")
        rtcom.broadcast_endpoint("perf", perf)
        rtcom.broadcast_endpoint("data", data)
        #rtcom.broadcast_endpoint("heartbeat", beat)

        #print(f"Network time: {time.perf_counter()-start}")
        perf["Network time"] = ((time.perf_counter()-start)*1000, "ms")
        start = time.perf_counter()

        

        pantilt.set_horizontal_angle(horizontal_angle)
        pantilt.set_vertical_angle(0)

        if "pc" in rtcom and "coordinates" in rtcom["pc"]:
            
            pantilt.set_vertical_angle(rtcom["pc"]["coordinates"]["vertical_angle"])

        beat+=1

        
        #time.sleep(0.020)
        data["Loop runtime"] = ((time.perf_counter()-loop_start_time)*1000, "ms")
        #loop_start_time=time.perf_counter()

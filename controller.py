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

def draw_and_broadcast(image, objs, labels, rtcom):
    pil_frame = Image.fromarray(image)
    draw_objects(ImageDraw.Draw(pil_frame), objs, labels)
    frame = np.array(pil_frame)
    frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
    
    encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 70]
    ret, jpg_image = cv2.imencode("*.jpg",frame, encode_param)

    rtcom.broadcast_endpoint("jpeg_image", bytes(jpg_image), encoding="binary")

from collections import deque

draw_broadcast_queue = deque(maxlen=1)

class DrawAndBroadcastThread(threading.Thread):
    def __init__(self):
      threading.Thread.__init__(self)

    def run(self):
        while True:
            try:
                args =  draw_broadcast_queue.pop()
                draw_and_broadcast(*args)
            except:
                time.sleep(0.05)
                

with RealTimeCommunication("turret.local") as rtcom:
    beat=0
    P = 0.05
    D = 0.05
    cap = VideoCapture(0)

    interpreter = make_interpreter("yolov8n_integer_quant.tflite")
    interpreter.allocate_tensors()

    draw_thread = DrawAndBroadcastThread()
    draw_thread.start()

    horizontal_angle=0
    vertical_angle=0
    hysteresis = 10
    lost=0
    last_horizontal_error=0

    first_pass = True
    labels = load_labels("data/coco_labels.txt")
    perf = {} 
    data = {}
    loop_start_time=0

    while(True):
        data["Cycle Time"] = ((time.perf_counter() - loop_start_time)*1000, "ms")
        loop_start_time=time.perf_counter()
        start = time.perf_counter()
        frame = cap.read()
        data["Capture time"] = ((time.perf_counter() - loop_start_time)*1000, "ms")
        start = time.perf_counter()
        
        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        size = (image.shape[1], image.shape[0])
        scale = detect.set_input(interpreter, size,
                           lambda size: cv2.resize(image, size,interpolation = cv2.INTER_NEAREST))

        data["Scaling time"] = ((time.perf_counter()-start)*1000, "ms")
        start = time.perf_counter()

        interpreter.invoke()
        objs = detect.get_output(interpreter, 0.4, scale)

        data["Inference time"] = ((time.perf_counter()-start)*1000, "ms")
        start = time.perf_counter()
        
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

        draw_broadcast_queue.append((image, objs, labels, rtcom))

        data["Broadcast time"] = ((time.perf_counter()-start)*1000, "ms")
        start = time.perf_counter()

        rtcom.broadcast_endpoint("perf", perf)
        rtcom.broadcast_endpoint("data", data)
        data["Network time"] = ((time.perf_counter()-start)*1000, "ms")
        start = time.perf_counter()

        pantilt.set_horizontal_angle(horizontal_angle)
        pantilt.set_vertical_angle(0)

        if "pc" in rtcom and "coordinates" in rtcom["pc"]:
            pantilt.set_vertical_angle(rtcom["pc"]["coordinates"]["vertical_angle"])

        data["Pantilt time"] = ((time.perf_counter()-start)*1000, "ms")
        beat+=1

        data["Loop runtime"] = ((time.perf_counter()-loop_start_time)*1000, "ms")

import picamera2
import tempfile
import os
from picamera2 import Picamera2
import time
import cv2
import numpy as np
def test_capture_single_jpeg():
    camera = Picamera2()
    # capture a single image
    #with tempfile.TemporaryDirectory() as tempdir:
    filename = os.path.join(".", "test.jpg")
    camera.start()
    camera.capture_file(filename)
    assert os.path.exists(filename)
    assert os.path.getsize(filename) > 0
    camera.stop()

def test_camera_get_image():
    camera = Picamera2()
    camera.start()
    image = camera.capture_array()
    assert image is not None
    camera.stop()
    assert isinstance(image, np.ndarray)
    assert image.shape == (480, 640, 4)
    assert image.dtype == np.uint8

    #save the image in a jpeg file
    filename = os.path.join(".", "test_array.jpg")
    cv2.imwrite(filename, image)





    
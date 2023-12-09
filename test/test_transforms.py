import pantilt
from time import sleep
import unittest
import math
import numpy as np
import transform
import psutil

#Test for coordinates transformations. 
class TestTransform(unittest.TestCase):
    def test_pixel_to_sensor_position_center(self):
        camera = transform.Camera()
        center = camera.pixel_to_sensor_position((320,240), (640,480))
        x,y = center
        self.assertAlmostEquals(x,0)
        self.assertAlmostEquals(y,0)

    def test_pixel_to_sensor_position_corner(self):
        camera = transform.Camera()
        corner = camera.pixel_to_sensor_position((0,0),(640,480))
        x,y = corner
        #3.674 x 2.760 mm
        self.assertAlmostEquals(round(x,3),-round(3.674/2, 3))
        self.assertAlmostEquals(round(y,3),-round(2.760/2, 3))

    def test_sensor_position_to_position_on_facing_plane(self):
        camera = transform.Camera()
        distance = 800
        x,y = camera.pixel_to_sensor_position((640/4,480/4),(640,480))
        x,y = camera.sensor_position_to_position_on_facing_plane((x,y), distance)
        self.assertAlmostEquals(round(x,3), -241.711)
        self.assertAlmostEquals(round(y,3), -181.579)
        
        


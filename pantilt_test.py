import pantilt
from time import sleep
import unittest
import math
import numpy as np
class TestPanTilt(unittest.TestCase):

    def test_angle_to_pwm(self):
        self.assertAlmostEquals(pantilt.angle_to_pwm(-90),500)
        self.assertAlmostEquals(pantilt.angle_to_pwm(90),2500)

    def test_center(self):
        pantilt.center()

    def circle(self):
        for x in np.arange(0,2*math.pi, math.pi/180):
            h_rad = math.sin(x) / 5
            v_rad = math.cos(x) / 5
            h = h_rad * 180 / math.pi
            v = v_rad * 180 / math.pi
            pantilt.set_horizontal_angle(h)
            pantilt.set_vertical_angle(v)
            sleep(0.01)
    
    def test_circle(self):
        pantilt.center()
        sleep(1)
        for _ in range(0,10):
            self.circle()

    def test_horizontal_sweep(self):
        for angle in range(-90,90):
            pantilt.set_horizontal_angle(angle)
            if angle==0:
                sleep(1)
            sleep(0.1)
    
    def test_vertical_sweep(self):
        for angle in range(-45,45):
            pantilt.set_vertical_angle(angle)
            if angle==0:
                sleep(1)
            sleep(0.1)

    @unittest.skip("Will cause mechanical interference")
    def test_raw_horizontal_sweep(self):
        for angle in range(-90,90):
            pantilt.set_raw_horizontal_angle(angle)
            sleep(0.1)
    
    @unittest.skip("Will cause mechanical interference")
    def test_raw_vertical_sweep(self):
        for angle in range(0,60):
            pantilt.set_raw_vertical_angle(angle)
            sleep(0.1)
        
if __name__ == '__main__':
    unittest.main()


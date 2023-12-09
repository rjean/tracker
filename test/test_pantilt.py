import turret.pantilt as pantilt
from time import sleep
import unittest
import math
import numpy as np
import pytest

def test_horizontal_position_to_angle(self):
    angle = pantilt.horizontal_position_to_angle(250, 800)
    self.assertAlmostEquals(round(angle,3),15.594)

def test_angle_to_pwm(self):
    self.assertAlmostEquals(pantilt.angle_to_pwm(-90),500)
    self.assertAlmostEquals(pantilt.angle_to_pwm(90),2500)

def test_center(self):
    pantilt.center()

def test_power_off(self):
    pantilt.power_off()

def circle(self):
    for x in np.arange(0,2*math.pi, math.pi/180):
        h_rad = math.sin(x) / 5
        v_rad = math.cos(x) / 5
        h = h_rad * 180 / math.pi
        v = v_rad * 180 / math.pi
        pantilt.set_horizontal_angle(h)
        pantilt.set_vertical_angle(v)
        sleep(0.01)

def test_square(self):
    pantilt.center()
    sleep(1)
    for _ in range(0,2):
        self.square()

def test_keypoints(self):
    # On a target, on the wall. Camera distance = 800 mm
    angle = pantilt.horizontal_position_to_angle(215.9/2, 600)
    # Aiming for the edge of a 8 1/2 x 11 sheet centered at 800mm
    pantilt.set_vertical_angle(0)
    pantilt.set_horizontal_angle(0)
    sleep(1)
    pantilt.set_horizontal_angle(angle)
    sleep(1)
    pantilt.set_horizontal_angle(-angle)

def square(self):
    pantilt.set_horizontal_angle(-10)
    pantilt.set_vertical_angle(-10)
    for h in np.arange(-10,10):
        pantilt.set_horizontal_angle(h)
        sleep(0.1)
    for v in np.arange(-10,10):
        pantilt.set_vertical_angle(v)
        sleep(0.1)
    for h in np.arange(10,-10,-1):
        pantilt.set_horizontal_angle(h)
        sleep(0.1)
    for v in np.arange(10,-10,-1):
        pantilt.set_vertical_angle(v)
        sleep(0.1)            

def test_circle(self):
    pantilt.center()
    sleep(1)
    for _ in range(0,2):
        self.circle()
    pantilt.center()
def test_horizontal_45(self):
    pantilt.set_horizontal_angle(45)
    
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

@pytest.mark.skip(reason="Will cause mechanical interference")
def test_raw_horizontal_sweep(self):
    for angle in range(-90,90):
        pantilt.set_raw_horizontal_angle(angle)
        sleep(0.1)

@pytest.mark.skip(reason="Will cause mechanical interference")
def test_raw_vertical_sweep(self):
    for angle in range(0,60):
        pantilt.set_raw_vertical_angle(angle)
        sleep(0.1)
    
if __name__ == '__main__':
    unittest.main()


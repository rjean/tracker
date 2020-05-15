import pantilt
from time import sleep
import unittest

class TestPanTilt(unittest.TestCase):

    def test_angle_to_pwm(self):
        self.assertAlmostEquals(pantilt.angle_to_pwm(-90),500)
        self.assertAlmostEquals(pantilt.angle_to_pwm(90),2500)

    def test_center(self):
        pantilt.center()
    
    def test_horizontal_sweep(self):
        for angle in range(-90,90):
            pantilt.set_horizontal_angle(angle)
            sleep(0.1)
    
    def test_vertical_sweep(self):
        for angle in range(0,60):
            pantilt.set_vertical_angle(angle)
            sleep(0.1)
        
if __name__ == '__main__':
    unittest.main()


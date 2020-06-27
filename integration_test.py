import pantilt
from time import sleep
import unittest
import math
import numpy as np

import psutil

#Integration Test Suite
class TestIntegration(unittest.TestCase):
    def check_if_process_is_running(self, name):
        for proc in psutil.process_iter(['pid', 'name']):
            if proc.info["name"]==name:
                return True
        return False

    def test_gpuiod_avaible(self):
        self.assertTrue(self.check_if_process_is_running("pigpiod"), 
        msg="pigpiod must be running for this program to work!")

#Real-time communications
import unittest
#import thread
from rtcom import *

from time import sleep
#Test for coordinates transformations. 
class TestRealTimeCommunication(unittest.TestCase):
    def test_test(self):
        self.assertTrue(True)
        
    def test_timeout(self):
        with RealTimeCommunication() as rtcom:
            sleep(1)
            self.assertEqual(rtcom.listen_thread.miss_counter,9)

    def test_device_message(self):
        with RealTimeCommunication("turret.local") as rtcom:
            rtcom.broadcast_endpoint("heartbeat", 10)
            sleep(0.1) 
            self.assertEqual(rtcom.listen_thread.devices["turret.local"].endpoints["heartbeat"].data, 10)
            self.assertEqual(rtcom["turret.local"]["heartbeat"],10)
            rtcom.broadcast_endpoint("heartbeat", 11)
            sleep(0.1) 
            self.assertEqual(rtcom.listen_thread.devices["turret.local"].endpoints["heartbeat"].data, 11)
            self.assertEqual(rtcom["turret.local"]["heartbeat"],11)
            rtcom.broadcast_endpoint("binary_data", bytes([1,2,3,4]), encoding="binary")
            sleep(0.1) 
            self.assertEqual(rtcom["turret.local"]["binary_data"],bytes([1,2,3,4]))
        
    def test_build_message_yaml(self):
        message = build_message("device", "endpoint", {"hello" : "world"}, "yaml")
        self.assertEqual(len(message),34)
        self.assertIsInstance(message, bytearray)

    def test_read_raw_message(self):
        message = build_message("device", "endpoint", {"hello" : "world"}, "yaml")
        header_line, data = read_raw_message(message)
        self.assertEqual(header_line,"device/endpoint:yaml")
        self.assertIsInstance(data, bytearray)
        self.assertEqual(len(data),13)

    def test_read_message(self):
        message = build_message("device", "endpoint", {"hello" : "world"}, "yaml")
        device, endpoint, data, encoding = read_message(message)
        self.assertEqual(device, "device")
        self.assertEqual(endpoint, "endpoint")
        self.assertEqual(encoding,"yaml")
        self.assertEqual(data, {"hello" : "world"})



if __name__ == '__main__':
    unittest.main()
#Real-time communications
import unittest
#import thread
from rtcom import *
import os
from time import sleep
#Test for coordinates transformations. 
class TestRealTimeCommunication(unittest.TestCase):
    def test_test(self):
        self.assertTrue(True)
        
    def test_timeout(self):
        with RealTimeCommunication() as rtcom:
            rtcom.write=False
            initial_miss = rtcom.listen_thread.miss_counter
            sleep(1)
            self.assertGreater(rtcom.listen_thread.miss_counter,initial_miss)

    def test_subscriptions(self):
        with RealTimeCommunication("test.device") as rtcom:
            rtcom.subscribe("test.device", "video_feed")
            sleep(0.1)
            subscribers = rtcom.get_subscribers()
            self.assertEqual(len(subscribers),1)
            self.assertEqual(subscribers["video_feed"], "test.device")
            
    def test_device_message(self):
        with RealTimeCommunication("test.device") as rtcom:
            rtcom.broadcast_endpoint("heartbeat", 10)
            sleep(0.2) 
            self.assertEqual(rtcom.listen_thread.devices["test.device"].endpoints["heartbeat"].data, 10)
            self.assertEqual(rtcom["test.device"]["heartbeat"],10)
            rtcom.broadcast_endpoint("heartbeat", 11)
            sleep(0.2)  
            self.assertEqual(rtcom.listen_thread.devices["test.device"].endpoints["heartbeat"].data, 11)
            self.assertEqual(rtcom["test.device"]["heartbeat"],11)
            rtcom.broadcast_endpoint("binary_data", bytes([1,2,3,4]), encoding="binary")
            sleep(0.2) 
            self.assertEqual(rtcom["test.device"]["binary_data"],bytes([1,2,3,4]))
        
    def test_build_message_yaml(self):
        message = build_message("device", "endpoint", {"hello" : "world"}, "yaml")[0]
        self.assertEqual(len(message),40)
        self.assertIsInstance(message, bytearray)

    def test_build_big_message(self):
        random_data=bytearray(os.urandom(12345)) 
        messages = build_message("device", "endpoint", random_data, "binary")
        input_buffer = None
        message_length=0
        for message in messages:
            device, endpoint, data, encoding, id, sequence, max_sequence = read_message(message)
            if input_buffer is None:
                input_buffer=bytearray(1000*max_sequence)
            input_buffer[sequence*1000:sequence*1000+len(data)]=data
            message_length+=len(data)
        received_data=input_buffer[0:message_length]
        self.assertEqual(len(received_data),12345)
        self.assertEqual(received_data, random_data)


    def test_big_message(self):
        with RealTimeCommunication("test.device") as rtcom:
            big_message = bytearray(os.urandom(60000)) 
            rtcom.broadcast_endpoint("image_data", big_message, encoding="binary")
            sleep(1)
            self.assertEqual(len(rtcom["test.device"]["image_data"]),60000)


    def test_read_raw_message(self):
        message = build_message("device", "endpoint", {"hello" : "world"}, "yaml")[0]
        header_line, data = read_raw_message(message)
        self.assertEqual(header_line,"device/endpoint:yaml:0:0:1")
        self.assertIsInstance(data, bytearray)
        self.assertEqual(len(data),13)



    def test_read_message(self):
        message = build_message("device", "endpoint", {"hello" : "world"}, "yaml")[0]
        device, endpoint, data, encoding, _, _, _ = read_message(message)
        self.assertEqual(device, "device")
        self.assertEqual(endpoint, "endpoint")
        self.assertEqual(encoding,"yaml")
        self.assertEqual(data, {"hello" : "world"})



if __name__ == '__main__':
    unittest.main()
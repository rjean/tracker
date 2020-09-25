#Real-time communications
import unittest
#import thread
from rtcom import RealTimeCommunication

from time import sleep
#Test for coordinates transformations. 
class TestRealTimeCommunication(unittest.TestCase):
    def test_test(self):
        self.assertTrue(True)
        
    def test_broadcast(self):
        rtcom = RealTimeCommunication()
        test_message = {"Hello" : "World"}
        rtcom.broadcast(test_message) 
        sleep(0.1)
        self.assertEqual(rtcom.listen_thread.json_data,test_message)
        rtcom.stop()


    def test_announce(self):
        rtcom = RealTimeCommunication("test_device")
        rtcom.announce()
        sleep(0.1)
        self.assertTrue("test_device" in rtcom.devices)
        rtcom.stop()

    def test_timeout(self):
        rtcom = RealTimeCommunication()
        sleep(1)
        self.assertEqual(rtcom.listen_thread.miss_counter,9)
        rtcom.stop() 

if __name__ == '__main__':
    unittest.main()
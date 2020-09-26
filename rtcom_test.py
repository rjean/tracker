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
        with RealTimeCommunication() as rtcom:
            test_message = {"Hello" : "World"}
            rtcom.broadcast(test_message) 
            sleep(0.1)
            self.assertEqual(rtcom.listen_thread.data_dict,test_message)


    def test_announce(self):
        with RealTimeCommunication("test_device") as rtcom:
            rtcom.announce()
            sleep(0.2)
            self.assertTrue("test_device" in rtcom.listen_thread.devices)

    def test_announce_turret(self):
        with RealTimeCommunication("turret.local") as rtcom:
            rtcom.announce()
            sleep(0.1)
            self.assertTrue("turret.local" in rtcom.listen_thread.devices)
 

    def test_timeout(self):
        with RealTimeCommunication() as rtcom:
            sleep(1)
            self.assertEqual(rtcom.listen_thread.miss_counter,9)

    def test_device_message(self):
        with RealTimeCommunication("turret.local") as rtcom:
            rtcom.announce()
            sleep(1) 
        x=1
        



if __name__ == '__main__':
    unittest.main()
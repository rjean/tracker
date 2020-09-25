import sched
import threading
import json
import socket
import time

class RealTimeCommunication:
    def __init__(self, device_name=None):
        if device_name is None:
            self.device_name = socket.gethostname()
        else:
            self.device_name = device_name

        self.endpoints = {}
        self.listen_thread = self.Listen(self)
        self.listen_thread.start()
        self.devices = {}
        

    def announce(self):
        message = {"announce" : 
                        {"device_name": self.device_name, 
                         "endpoints" : self.endpoints}}
        self.broadcast(message)

    def broadcast(self, message, port=5999):
        sock = socket.socket(socket.AF_INET, # Internet
                             socket.SOCK_DGRAM) # UDP
        json_message = json.dumps(message)
        data = json_message.encode('utf-8')
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        sock.sendto(data, ("255.255.255.255", port))
        sock.close()

    def stop(self):
        self.listen_thread.enabled=False
        self.listen_thread.join()

    class Listen(threading.Thread):
        def __init__(self, rtcom, port=5999, hostname=None):
            threading.Thread.__init__(self)
            if hostname is None:
                UDP_IP = "0.0.0.0"
            self.sock = socket.socket(socket.AF_INET, # Internet
                                 socket.SOCK_DGRAM) # UDP
            self.sock.bind((UDP_IP, port))
            self.sock.settimeout(0.1)
            self.json_data=None
            self.enabled=True
            self.miss_counter=0
            self.rtcom = rtcom


        def run(self):
            while self.enabled:
                try:
                    data, addr = self.sock.recvfrom(1024) # buffer size is 1024 bytes
                    json_data = json.loads(data)
                    self.json_data = json_data
                    if "announce" in json_data:
                        device_name = json_data["announce"]["device_name"]
                        self.rtcom.devices[device_name] = json_data["announce"]["endpoints"]
                        
                    self.miss_counter=0
                    print("received message: %s" % self.json_data)
                except:
                    self.miss_counter+=1
            self.sock.close()
                #print(addr)

#rtcom = RealTimeCommunication()
#while True:
#    rtcom.broadcast({"Hello" :"World!"})


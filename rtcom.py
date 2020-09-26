import sched
import threading
import yaml
import socket
import time

class Device():
    def __init__(self, name, addr):
        threading.Thread.__init__(self)
        self.name=name
        self.addr=addr
        self.broadcast = False
        self.enabled = True
        #self.rtcom = rtcom
        self.messages = {}
    

class RealTimeCommunication:
    def __init__(self, device_name=None):
        if device_name is None:
            self.device_name = socket.gethostname()
        else:
            self.device_name = device_name
        try:
            addr = socket.gethostbyname(self.device_name)
        except:
            addr = "127.0.0.1"

        self.this_device = Device(self.device_name, addr)

        self.endpoints = {}
        self.listen_thread = RealTimeCommunicationListener(self)
        self.listen_thread.start()
        self.devices = {}

    def __enter__(self):
        return self
        
    def announce(self):
        message = {"announce" : 
                        {"device_name": self.device_name, 
                         "endpoints" : self.endpoints}}
        self.broadcast(message)

    def broadcast(self, message, port=5999):
        sock = socket.socket(socket.AF_INET, # Internet
                             socket.SOCK_DGRAM) # UDP
        encoded_message = yaml.dump(message)
        data = encoded_message.encode('utf-8')
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        sock.sendto(data, ("255.255.255.255", port))
        sock.close()

    def __exit__(self, exc_type, exc_value, traceback):
        self.listen_thread.enabled=False
        self.listen_thread.join()


class RealTimeCommunicationListener(threading.Thread):
    def __init__(self, rtcom, port=5999, hostname=None):
        threading.Thread.__init__(self)
        if hostname is None:
            UDP_IP = "0.0.0.0"
        print(f"Listening to {UDP_IP}")
        self.sock = socket.socket(socket.AF_INET, # Internet
                             socket.SOCK_DGRAM) # UDP
        self.sock.bind((UDP_IP, port))
        self.sock.settimeout(0.1)
        self.data_dict=None
        self.enabled=True
        self.miss_counter=0
        self.rtcom = rtcom
        self.devices = {}

    def run(self):
        while self.enabled:
            try:
                data, addr = self.sock.recvfrom(1024) # buffer size is 1024 bytes
                data_dict = yaml.load(data, Loader=yaml.Loader)
                self.data_dict = data_dict
                if "announce" in data_dict:
                    device_name = data_dict["announce"]["device_name"]
                    if device_name not in self.devices:
                        self.devices[device_name] = Device(device_name, addr)                        
                self.miss_counter=0
                print("received message: %s" % self.data_dict)
            except:
                self.miss_counter+=1
        self.sock.close()
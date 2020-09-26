import sched
import threading
import yaml
import socket
import time
import re

def read_raw_message(data):
    for i in range(len(data)):
        if data[i]==ord('\n'):
            return data[0:i].decode("utf-8"), data[i+1:]
    raise ValueError("Unable to find the end of line")

def read_message(data):
    header, data = read_raw_message(data)
    #'device/endpoint:encoding'
    match = re.search("(.*?)/(.*?):(.*)", header)
    device = match[1]
    endpoint = match[2]
    encoding = match[3]
    if encoding=="yaml":
        data = yaml.load(data.decode("utf-8"))
    return device, endpoint, data, encoding

def build_message(device_name, endpoint, data, encoding):
        header = bytes(f"{device_name}/{endpoint}:{encoding}\n", "utf-8")
        if encoding=="yaml":
            encoded_data = bytes(yaml.dump(data), "utf-8")
        elif encoding=="binary":
            encoded_data = data
        else:
            raise ValueError("Please specify a supported encoding methods. (binary or yaml)")

        size = len(header) + len(encoded_data)
        message = bytearray(size)
        message[0:len(header)]=header
        message[len(header):]=encoded_data
        return message

class Device():
    def __init__(self, name, addr):
        self.name=name
        self.addr=addr
        self.broadcast = False
        self.enabled = True
        #self.rtcom = rtcom
        self.endpoints = {}
    
    def __getitem__(self, key):
        return self.endpoints[key].data

class Endpoint():
    def __init__(self, name, encoding, data = None):
        self.name = name
        self.encoding = encoding
        self.data = data

    

class RealTimeCommunication:
    def __init__(self, device_name=None, listen=True):
        if device_name is None:
            self.device_name = socket.gethostname()
        else:
            self.device_name = device_name
        try:
            addr = socket.gethostbyname(self.device_name)
        except:
            addr = "127.0.0.1"

        self.listen=listen
        self.this_device = Device(self.device_name, addr)

        self.endpoints = {}
        if listen:
            self.listen_thread = RealTimeCommunicationListener(self)
            self.listen_thread.start()
        self.devices = {}

    def __getitem__(self, key):
        return self.listen_thread.devices[key]

    def __enter__(self):
        return self
        
    def announce(self):
        message = {"announce" : 
                        {"device_name": self.device_name, 
                         "endpoints" : self.endpoints}}
        self.broadcast(message)

    def broadcast(self, data, port=5999):
        sock = socket.socket(socket.AF_INET, # Internet
                             socket.SOCK_DGRAM) # UDP
        #encoded_message = yaml.dump(message)
        #data = encoded_message.encode('utf-8')
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        sock.sendto(data, ("255.255.255.255", port))
        sock.close()

    def broadcast_endpoint(self, endpoint, data, encoding="yaml"):
        message = build_message(self.device_name, endpoint, data, encoding)
        self.broadcast(message)

    def __exit__(self, exc_type, exc_value, traceback):
        if self.listen:
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
                data, addr = self.sock.recvfrom(65000) # buffer size is 1024 bytes
                device, endpoint, data, encoding = read_message(data)
                if device not in self.devices:
                    self.devices[device] = Device(device, addr)
                
                if endpoint not in self.devices[device].endpoints:
                    self.devices[device].endpoints[endpoint] = Endpoint(endpoint, encoding, data)
                else:
                    self.devices[device].endpoints[endpoint].data = data
                    
                # data_dict = yaml.load(data, Loader=yaml.Loader)
                # self.data_dict = data_dict
                # if "announce" in data_dict:
                #    device_name = data_dict["announce"]["device_name"]
                #    if device_name not in self.devices:
                                              
                self.miss_counter=0
                print(f"{device}, {endpoint}, {encoding}, {len(data)}")
            except:
                self.miss_counter+=1
        self.sock.close()
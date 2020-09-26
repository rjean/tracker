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
    #'device/endpoint:encoding:id:sequence'
    match = re.search("(.*?)/(.*?):(.*?):(.*?):(.*?):(.*)", header)
    device = match[1]
    endpoint = match[2]
    encoding = match[3]
    id = match[4]
    sequence = match[5]
    max_sequence = match[6]
    if encoding=="yaml":
        data = yaml.load(data.decode("utf-8"))
    return device, endpoint, data, encoding, int(id), int(sequence), int(max_sequence)

def build_message(device_name, endpoint, data, encoding, id=0, max_size=1000):
    messages = []
    if encoding=="yaml":
        encoded_data = bytes(yaml.dump(data), "utf-8")
    elif encoding=="binary":
        encoded_data = data
    else:
        raise ValueError("Please specify a supported encoding methods. (binary or yaml)")
    number_of_messages = int(len(encoded_data)/max_size)+1
    if len(encoded_data)%max_size==0:
        number_of_messages-=1

    remaining_bytes = len(encoded_data)
    
    for sequence in range(number_of_messages):
        header = bytes(f"{device_name}/{endpoint}:{encoding}:{id}:{sequence}:{number_of_messages}\n", "utf-8")
        size = len(header) + min(remaining_bytes, max_size)
        message = bytearray(size)
        message[0:len(header)]=header
        message[len(header):size]=encoded_data[sequence*max_size:sequence*max_size+min(remaining_bytes, max_size)]
        remaining_bytes=remaining_bytes-max_size
        messages.append(message)
    return messages

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

    def __contains__(self, key):
        return key in self.endpoints

class Endpoint():
    def __init__(self, name, encoding, data = None):
        self.name = name
        self.encoding = encoding
        self.data = data
        self.next_data = {}
        self.transmission_id = -1 #Current transmission id

    

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

    def __contains__(self, key):
        return key in self.listen_thread.devices
        
    def announce(self):
        message = {"announce" : 
                        {"device_name": self.device_name, 
                         "endpoints" : self.endpoints}}
        self.broadcast(message)

    def broadcast(self, packets, port=5999, addr=None):
        sock = socket.socket(socket.AF_INET, # Internet
                             socket.SOCK_DGRAM) # UDP
        #encoded_message = yaml.dump(message)
        #data = encoded_message.encode('utf-8')
        if addr is None:
            addr= "255.255.255.255"
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        for data in packets:
            sock.sendto(data, (addr, port))
        sock.close()

    def broadcast_endpoint(self, endpoint, data, encoding="yaml", addr=None):
        if endpoint not in self.endpoints:
            self.endpoints[endpoint]=0
        else:
            self.endpoints[endpoint]+=1
        packets = build_message(self.device_name, endpoint, data, encoding, id=self.endpoints[endpoint])
        self.broadcast(packets, addr=addr)
        #for packet in packets:
        #    self.broadcast(packet)
        

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
                data, addr = self.sock.recvfrom(1500) # buffer size is 1024 bytes
                device, endpoint, data, encoding, id, sequence, max_sequence = read_message(data)
                if device not in self.devices:
                    self.devices[device] = Device(device, addr)
                
                if max_sequence==1:
                    if endpoint not in self.devices[device].endpoints:
                        self.devices[device].endpoints[endpoint] = Endpoint(endpoint, encoding, data)
                    else:
                        self.devices[device].endpoints[endpoint].data = data
                else:
                    #Handle big messages
                    if endpoint not in self.devices[device].endpoints:
                        self.devices[device].endpoints[endpoint] = Endpoint(endpoint, encoding)
                    
                    if id != self.devices[device].endpoints[endpoint].transmission_id:
                        self.devices[device].endpoints[endpoint].next_data={}
                        self.devices[device].endpoints[endpoint].transmission_id=id
                    self.devices[device].endpoints[endpoint].next_data[sequence] = data
                    ready=True
                    for i in range(0,max_sequence):
                        if i not in self.devices[device].endpoints[endpoint].next_data:
                            ready=False
                            break
                    message_length=0
                    if ready:
                        print("ready")
                        input_buffer=bytearray(1000*max_sequence)
                        for i in range(0,max_sequence):
                            data = self.devices[device].endpoints[endpoint].next_data[i]
                            input_buffer[i*1000:i*1000+len(data)]=data
                            message_length+=len(data)
                        self.devices[device].endpoints[endpoint].data = input_buffer[0:message_length]
                       
                self.miss_counter=0
                print(f"{device}, {endpoint}, {encoding}, {id},{sequence}, {max_sequence}")
            except:
                self.miss_counter+=1
        self.sock.close()
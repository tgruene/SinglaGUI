import json

import zmq
import socket as so

context = zmq.Context()

#  Socket to talk to server
print("Connecting to hello world server…")
socket = context.socket(zmq.PULL)
socket.connect("tcp://localhost:4545")
print("Connection established")


# s = so.socket()
# s.connect(("singla-dcu", 9999))

while True:
    print ("Waiting for socket")
    packet = socket.recv()
    print ("Socket received")
    if packet[0] == 123: # if the packet begins with "{" character:
        packet = json.loads(packet)
    else:
        print(packet[0])
        continue

    if packet["htype"] == "dheader-1.0":
        if packet["header_detail"] == "all" or packet["header_detail"] == "basic":
            config_params = socket.recv_json()

        if packet["header_detail"] == "all":
            flatfield_header = socket.recv_json()
            flatfield_data = socket.recv()

            pixelmask_header = socket.recv_json()
            pixelmask_data = socket.recv()

            countrate_header = socket.recv_json()
            countrate_data = socket.recv()

    if packet["htype"] == "dimage-1.0":
        print("receiving image...")
        data_header = socket.recv_json()
        image_data = socket.recv()
        config_header = socket.recv_json()
        print(data_header, config_header, image_data[0: 15])

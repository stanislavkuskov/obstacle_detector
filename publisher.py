import time
import zmq

from base import BaseThread


class Publisher(BaseThread):
    def __init__(self, port="5555", topic="obstacle_detector"):
        super().__init__()
        port = port
        context = zmq.Context()
        self.socket = context.socket(zmq.PUB)
        self.socket.bind("tcp://*:%s" % port)
        self.topic = topic
        self.objects_dict = None
        self.previous_object_dict = None

    def run(self):
        while not self.is_stopped:

            if self.objects_dict:
                if self.objects_dict != self.previous_object_dict:
                    self.socket.send_string(self.topic, zmq.SNDMORE)
                    self.socket.send_pyobj(self.objects_dict)
                    self.previous_object_dict = self.objects_dict

    @property
    def return_objects_dict(self):
        return self.objects_dict

    @return_objects_dict.setter
    def return_objects_dict(self, value):
        self.objects_dict = value

# Subscriber example for receiving messages from this publisher.
# ... Necessarily read topic (same with publisher)

# from time import sleep
# import zmq
#
# topic = b'obstacle_detector'
# context = zmq.Context()
# socket = context.socket(zmq.SUB)
# socket.connect("tcp://localhost:5555")
# socket.setsockopt(zmq.SUBSCRIBE, topic)
# sleep(1)
# while True:
#     topic = socket.recv_string()
#     objects_dict = socket.recv_pyobj()
#     print(objects_dict)

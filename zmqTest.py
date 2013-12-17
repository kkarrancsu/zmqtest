#!/usr/bin/python
# -*- coding: utf-8 -*-

# a simple program to figure out what is going on between threading and
# process for ZMQ

import zmq
import threading
import time
import multiprocessing

class MainClass:
    def __init__(self):
        port = 11112
        s = SenderClass(port)
        r = ReceiverClass(port)
        s.start()
        r.start()

# class SenderClass(threading.Thread):
class SenderClass(multiprocessing.Process):
    def __init__(self, port):
        self.zmqContext = zmq.Context()
        self.pushSocket = self.zmqContext.socket(zmq.PUSH)
        self.pushSocket.bind('tcp://*:' + str(port))

#         threading.Thread.__init__(self)
        multiprocessing.Process.__init__(self)

        print 'sender init'

    def run(self):
        print 'sender running'
        for ii in range(0,10):
            print 'sent ' + str(ii)
            self.pushSocket.send(str(ii))
            time.sleep(1)
        self.pushSocket.send('KILL')

# class ReceiverClass(threading.Thread):
class ReceiverClass(multiprocessing.Process):
    def __init__(self, port):
        self.zmqContext = zmq.Context()
        self.pullSocket = self.zmqContext.socket(zmq.PULL)
        self.pullSocket.connect('tcp://localhost:' + str(port))

#         threading.Thread.__init__(self)
        multiprocessing.Process.__init__(self)

        print 'rx init'

    def run(self):
        print 'rx running'
        while True:
            rx = self.pullSocket.recv()
            if rx=='KILL':
                break;
            print 'received = ' + rx

if __name__=='__main__':
    M = MainClass()

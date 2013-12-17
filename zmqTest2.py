#!/usr/bin/python

import multiprocessing
import zmq
import threading
import time

class SenderClass(multiprocessing.Process):
# class SenderClass(threading.Thread):

    def __init__(self, port):
        self.zmqContext = zmq.Context()
        self.zmqSock = self.zmqContext.socket(zmq.PUSH)
        self.zmqSock.bind('tcp://*:' + str(port))

#         threading.Thread.__init__(self)
        multiprocessing.Process.__init__(self)

    def run(self):
        cnt = 1
        while (cnt<10):

            dataToSend = '3.14159286'
            print 'Sending (SenderClass)'
            # send that data over ZMQ
            try:
                self.zmqSock.send(dataToSend, zmq.NOBLOCK)
            except Exception, e:
                print e

            time.sleep(3)
            cnt = cnt + 1

        self.zmqSock.send('KILL', zmq.NOBLOCK)
        self.zmqSock.setsockopt(zmq.LINGER, 0)  # Terminate early
        self.zmqSock.close()

class RxClass(multiprocessing.Process):
# class RxClass(threading.Thread):

    def __init__(self, port):
        self.zmqContext = zmq.Context()
        self.zmqSock = self.zmqContext.socket(zmq.PULL)
        self.zmqSock.bind('tcp://*:' + str(port))

#         threading.Thread.__init__(self)
        multiprocessing.Process.__init__(self)

    def run(self):
        while True:
            # send that data over ZMQ
            try:
                rx = self.zmqSock.recv()
                print 'Received (RxClass) = ' + str(rx)
                if(rx=='KILL'):
                    break
            except Exception, e:
                print e

        self.zmqSock.setsockopt(zmq.LINGER, 0)  # Terminate early
        self.zmqSock.close()

class CPPClass(multiprocessing.Process):
# class CPPClass(threading.Thread):
    def __init__(self, sendPort, rxPort):

        self.zmqContext = zmq.Context()
        self.rxSock = self.zmqContext.socket(zmq.PULL)
        self.rxSock.connect('tcp://localhost:' + str(sendPort))

        self.txSock = self.zmqContext.socket(zmq.PUSH)
        self.txSock.connect('tcp://localhost:' + str(rxPort))

        multiprocessing.Process.__init__(self)
#         threading.Thread.__init__(self)

    def run(self):
        while True:
            # receive it
            rx = self.rxSock.recv()
            print 'Received (CPPClass) = ' + str(rx)

            # wait a bit
            time.sleep(1)

            # send it back out
            self.txSock.send(rx)
            print 'Sent (CPPClass)'

            if(rx=='KILL'):
                break

if __name__=="__main__":
    sendPort = 6555
    rxPort = 6556

    s = SenderClass(sendPort)
    r = RxClass(rxPort)
    time.sleep(1)

    c = CPPClass(sendPort, rxPort)

    time.sleep(1)
    c.start()
    r.start()
    s.start()


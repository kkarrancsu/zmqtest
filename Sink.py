#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Task sink
# Binds PULL socket to tcp://localhost:5558
# Collects results from workers via that socket
#
# Author: Lev Givon <lev(at)columbia(dot)edu>

import sys
import time
import zmq

import multiprocessing

class Sink(multiprocessing.Process):
    def __init__(self):
        super(Sink, self).__init__()

    def run(self):

        context = zmq.Context()

        # Socket to receive messages on
        receiver = context.socket(zmq.PULL)
        receiver.bind("tcp://*:6558")

        print 'waiting to receive'
        # Wait for start of batch
        s = receiver.recv()
        print 'received = ' + str(s)

        # Start our clock now
        tstart = time.time()

        # Process 100 confirmations
        total_msec = 0
        for task_nbr in range(100):
            s = receiver.recv()
            if task_nbr % 10 == 0:
                sys.stdout.write(':')
            else:
                sys.stdout.write('.')
            sys.stdout.flush()

        # Calculate and report duration of batch
        tend = time.time()
        print "Total elapsed time: %d msec" % ((tend-tstart)*1000)

if __name__=='__main__':
    s = Sink()
    s.start()

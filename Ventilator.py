#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Task ventilator
# Binds PUSH socket to tcp://localhost:5557
# Sends batch of tasks to workers via that socket
#
# Author: Lev Givon <lev(at)columbia(dot)edu>

import zmq
import random
import time

import multiprocessing

class Ventilator(multiprocessing.Process):
    def __init__(self):
        super(Ventilator, self).__init__()

    def run(self):
        context = zmq.Context()

        # Socket to send messages on
        sender = context.socket(zmq.PUSH)
        sender.bind("tcp://*:6557")

        # Socket with direct access to the sink: used to syncronize start of batch
        sink = context.socket(zmq.PUSH)
        sink.connect("tcp://localhost:5558")

        print "Sending tasks to workers�"

        # The first message is "0" and signals start of batch
        sink.send('0')

        # Initialize random number generator
        random.seed()

        # Send 100 tasks
        total_msec = 0
        for task_nbr in range(100):

            # Random workload from 1 to 100 msecs
            workload = random.randint(1, 100)
            total_msec += workload

            print 'sending workload = ' + str(workload)
            sender.send(str(workload))
            print 'workload sent!'

        print "Total expected cost: %s msec" % total_msec

        # Give 0MQ time to deliver
        time.sleep(1)


if __name__=='__main__':
    v = Ventilator()
    v.start()

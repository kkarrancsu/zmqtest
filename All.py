#!/usr/bin/env python
# -*- coding: utf-8 -*-

import Ventilator
import Sink
import subprocess

import time
import os

class All:
    def __init__(self):
        self.v = Ventilator.Ventilator()
        self.s = Sink.Sink()


    def runTheStuff(self):

        self.s.start()
        print 'sink started'
        self.v.start()
        print 'ventilator started'

        time.sleep(2)


        # start the algo
        h = subprocess.Popen(['./launchTest.sh'], close_fds=True)
#         os.system('./launchTest.sh')
        print 'test started'
#         time.sleep(2)

        time.sleep(10)
        h.kill()
        self.v.terminate()
        self.s.terminate()

        print 'killed everything'


if __name__=='__main__':
    a = All()
    a.runTheStuff()

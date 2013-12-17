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


#         # start the algo
#         h = subprocess.Popen(['test'], shell=True)
# #         os.system('test')
#         print 'test started'
# #         time.sleep(2)


if __name__=='__main__':
    a = All()
    a.runTheStuff()

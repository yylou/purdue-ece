#!/usr/bin/env python3
#
#    Author : Yuan-Yao Lou (Mike) <yylou@purdue.edu>
#    Title  : Ph.D. student in ECE at Purdue University
#    Date   : 2021/10/24
#


import os as OS
import sys as SYS
import datetime as DATETIME
import time as TIME
import subprocess as SUBP
from threading import Thread as THREAD


ROOT_PATH = OS.path.dirname(OS.path.abspath(__file__))

def sender():
    # SUBP.call(f'cd "{ROOT_PATH}/../\"Student\ Code\"/student"     && make run-sender   config=../../TestConfig/config4.ini', shell=True)
    SUBP.call(f'cd "{ROOT_PATH}/../\"Student\ Code\"/stop_and_go" && make run-sender   config=../../TestConfig/config4.ini', shell=True)

def receiver():
    # SUBP.call(f'cd "{ROOT_PATH}/../\"Student\ Code\"/student"     && make run-receiver config=../../TestConfig/config4.ini', shell=True)
    SUBP.call(f'cd "{ROOT_PATH}/../\"Student\ Code\"/stop_and_go" && make run-receiver config=../../TestConfig/config4.ini', shell=True)

def emulator():
    SUBP.call(f'cd "{ROOT_PATH}/../Emulator" && python3 emulator.py ../TestConfig/config4.ini', shell=True)

def dump_performance(timestamp):
    # SUBP.call(f'cd "{ROOT_PATH}/../\"Student\ Code\"/student"     && cat log/*{timestamp}.log', shell=True)
    SUBP.call(f'cd "{ROOT_PATH}/../\"Student\ Code\"/stop_and_go" && cat log/*{timestamp}.log', shell=True)

CONFIG_FILE = open('../TestConfig/config4.ini', 'r')
CONTENT = CONFIG_FILE.readlines()
CONFIG_FILE.close()

for _ in range(int(SYS.argv[1])):
    print( '------------------------------------------')
    print(f'Iteration: {_}')
    print( '------------------------------------------')

    TIMESTAMP = "{0:%Y-%m-%d-%H-%M-%S}".format(DATETIME.datetime.now())
    with open('../TestConfig/config4.ini', 'w') as FILE:
        for line in CONTENT:
            if 'log_file' not in line: FILE.write(line)
            else: 
                if   'sender'   in line: FILE.write(f'log_file=./log/sender_monitor-{TIMESTAMP}.log\n')
                elif 'receiver' in line: FILE.write(f'log_file=./log/receiver_monitor-{TIMESTAMP}.log\n')
                elif 'emulator' in line: FILE.write(f'log_file=./emulator-{TIMESTAMP}.log\n')

    thread_emul = THREAD(target=emulator, args=[])
    thread_emul.start()
    TIME.sleep(1)
    thread_recv = THREAD(target=receiver, args=[])
    thread_recv.start()
    TIME.sleep(2)
    thread_send = THREAD(target=sender,   args=[])
    thread_send.start()

    thread_emul.join(timeout=50)
    thread_recv.join(timeout=50)
    thread_send.join(timeout=50)

    thread_check = THREAD(target=dump_performance, args=[TIMESTAMP])
    thread_check.start()
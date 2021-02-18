#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import threading
import time;
import datetime;
import traceback;
import logging
from PyQt5 import QtWidgets
from qt.mainui import MainUI
from queue import Queue

from qt.log import LOG_PRINTF

from app.getgps import GetGPS

APP_NAME='imgacctest'

class MainThread:
    def __init__(self,mtq,qtq):
        self.mtq=mtq
        self.qtq=qtq

    def _cmd_start(self,data):
        LOG_PRINTF("[start]")
        qmsg = {'cmd':'progress',"data":10}
        self.qtq.put(qmsg)
        inFiles=data['inFiles']
        ouFiles=data['ouFiles']
        datatype = data['datatype']

        LOG_PRINTF("inFiles: " + inFiles)
        LOG_PRINTF("ouFiles: " + ouFiles)
        LOG_PRINTF("datatype: " + datatype)

        #extern interface add
        try:
            mm =GetGPS ();
            mm.run(inFiles,ouFiles,datatype)
        except:
            traceback.print_exc()

        time.sleep(1)
        qmsg.clear()
        qmsg = {'cmd': 'progress', "data": 99}
        self.qtq.put(qmsg)
        time.sleep(1)
        qmsg.clear()
        qmsg = {'cmd': 'finish'}
        self.qtq.put(qmsg)
        LOG_PRINTF("[finish]")

    def _cmd_close(self):
        print('_cmd_close')

    def run_thread(self):

        while True:
            if not self.mtq.empty():
                msg = self.mtq.get()
                if len(msg) > 0:
                    print('MainThread:',msg)
                    if msg['cmd'] == 'start':

                        self.th_run = threading.Thread(target=self._cmd_start, name="_cmd_start",args=(msg,))
                        self.th_run.setDaemon(True)
                        self.th_run.start()

                    elif msg['cmd'] == 'close':
                        self._cmd_close();

            else:
                time.sleep(1);

    def start(self):
        self.th_run = threading.Thread(target=self.run_thread, name="run_thread")
        self.th_run.setDaemon(True)
        self.th_run.start()


def run():


    mtq = Queue(100)
    qtq = Queue(100)

    mtobj=MainThread(mtq,qtq)
    mtobj.start();

    app = QtWidgets.QApplication(sys.argv)
    mmui=MainUI(mtq,qtq)
    mmui.show()
    #mmui.start()
    sys.exit(app.exec_())



def init():
    #format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    logdir=r'f:\log'
    logfile=None

    now_time = datetime.datetime.now()
    time1_str = datetime.datetime.strftime(now_time, '%Y%m%dT%H%M%S')

    logfilename='log_'+APP_NAME+'_'+time1_str+'.txt'

    if os.path.exists(logdir):
        logfile=os.path.join(logdir,logfilename)
    else:
        logfile=logfilename

    logger = logging.getLogger()  # 不加名称设置root logger
    logging.basicConfig(level=logging.INFO,format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    # 使用FileHandler输出到文件
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s: - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S')

    fh = logging.FileHandler(logfile)
    fh.setLevel(logging.DEBUG)
    fh.setFormatter(formatter)

    # 使用StreamHandler输出到屏幕
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    ch.setFormatter(formatter)

    # 添加两个Handler
    logger.addHandler(ch)
    logger.addHandler(fh)


if __name__ == '__main__':
    init();
    run()




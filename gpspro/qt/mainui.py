#!/usr/bin/env python
# -*- coding: utf-8 -*-


import os

import threading
import time
from queue import Queue

from time import sleep
from PyQt5 import QtCore, QtWidgets, QtGui

from .mainwindowapp import MainWindowApp

class MainUI(QtWidgets.QMainWindow,MainWindowApp):
    def __init__(self,mtq,qtq):
        super(MainUI, self).__init__()
        self.setupUi(self)
        self.mtq = mtq
        self.qtq = qtq

        self.init();

        self.mwapp_int(self.mtq)

    def closeEvent(self, a0: QtGui.QCloseEvent):
        super();
        print('closeEvent')

        qmsg = {'cmd':'close'}
        self.mtq.put(qmsg)


    def init(self):
        self.th_run = threading.Thread(target=self.run_thread, name="run_thread")
        self.th_run.setDaemon(True)
        self.th_run.start()

    def run_thread(self):
        while True:
            if not self.qtq.empty():
                msg = self.qtq.get()
                if len(msg) > 0:
                    print(msg)
                    if msg['cmd'] == 'progress':
                        pvalue=msg['data'];
                        self.mwapp_update_progress(pvalue)
                    if msg['cmd'] == 'finish':
                        self.mwapp_finish()

            else:
                time.sleep(1)








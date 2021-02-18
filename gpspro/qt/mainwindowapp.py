#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import os

import socket
import threading
import random
import time
import  traceback

import qt

from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

from PyQt5.QtCore import QObject, pyqtSlot, pyqtSignal

from queue import Queue

from .mainwindow import Ui_MainWindow
from .log import LOG_PRINTF

class MainWindowApp(Ui_MainWindow):

    updateprogresssig = QtCore.pyqtSignal(int)

    def __init__(self):
        super(MainWindowApp, self).__init__()
        self.inFiles=None;
        self.ouFiles=None;
        self.th_run=None
        self.mtq = None;

    def mwapp_int(self,mtq):
        self.mtq = mtq;

        self.pushButton_inFiles.clicked.connect(self.openinFiles)
        self.pushButton_outFiles.clicked.connect(self.openoutFiles)
        self.pushButton_start.clicked.connect(self.start)
        self.pushButton_cancel.clicked.connect(self.cancel)


        self.updateprogresssig.connect(self.progressBar_main.setValue)

        self.log_thread_status=1
        self.th_log = threading.Thread(target=self.log_thread, name="log_thread")
        self.th_log.setDaemon(True)
        self.th_log.start()



    def openinFiles(self):
        openfiles_name = QFileDialog.getExistingDirectory(self, '选择工程文件夹', '/')
        print(openfiles_name)
        if len(openfiles_name) > 0:
            self.lineEdit_inFiles.setText(openfiles_name);
            self.inFiles=openfiles_name;
            (filepath, tempfilename) = os.path.split(openfiles_name);
            if len(filepath) > 0 :
                self.ouFiles = filepath;
            else :
                self.ouFiles=openfiles_name;

            self.ouFiles=os.path.join(self.ouFiles,"out")
            self.lineEdit_outFiles.setText(self.ouFiles);


    def openoutFiles(self):
        openfiles_name = QFileDialog.getExistingDirectory(self, '选择输出文件夹', '/')
        print(openfiles_name)
        if len(openfiles_name) > 0:
            self.lineEdit_outFiles.setText(openfiles_name);

    def getsetdata(self):
        openfiles_name = self.lineEdit_inFiles.text();
        outfiles_name = self.lineEdit_outFiles.text();

        self.inFiles = openfiles_name;
        self.ouFiles = outfiles_name;
        if self.ouFiles == None or len(self.ouFiles) == 0:
            (filepath, tempfilename) = os.path.split(openfiles_name);
            if len(filepath) > 0:
                self.ouFiles = filepath;
            else:
                self.ouFiles = openfiles_name;

            self.ouFiles = os.path.join(self.ouFiles, "out")
            self.lineEdit_outFiles.setText(self.ouFiles);

        if self.inFiles == None:
            LOG_PRINTF('Input : [  None ]' + "  file not exists\n")
            return None

        if not os.path.exists(self.inFiles):
            LOG_PRINTF('Input:  '+'['+self.inFiles+']'+"  file not exists\n")
            return  None;

        self.datatype=self.comboBox_datatype.currentText();
     #   self.interval=self.comboBox_interval.currentText();

        msgq = { 'inFiles': self.inFiles, 'ouFiles': self.ouFiles, 'datatype':self.datatype};
        return msgq;

    def start(self):
        self.pushButton_start.setEnabled(False)
        self.progressBar_main.setValue(1)



        if self.mtq != None:
            msgq = self.getsetdata();
            msgq['cmd']='start'
            self.mtq.put(msgq)




    def cancel(self):
        self.pushButton_start.setEnabled(True)
        self.progressBar_main.setValue(0)

        if self.mtq != None:
            msgq={'cmd':'stop','inFiles':self.inFiles,'ouFiles':self.ouFiles};
            self.mtq.put(msgq)

    def mwapp_finish(self):

        try:
            self.pushButton_start.setEnabled(True)
            self.updateprogresssig.emit(100);
        #    self.progressBar_main.update()
            #self.progressBar_main.setValue(100)
        except:
            traceback.print_exc()


    def mwapp_update_progress(self,value):

        try:
            self.progressBar_main.setValue(int(value))
        except:
            traceback.print_exc()

    def run_thread(self):
        self.srcfile=self.lineEdit_inFiles.text();
        if not os.path.exists(self.srcfile):

            LOG_PRINTF('['+self.srcfile+']'+"  file not exists\n")
            return ;
        (filepath, tempfilename) = os.path.split(self.srcfile);
        (shotname, extension) = os.path.splitext(tempfilename);
        dstfilename=shotname+'_out'+".txt"
        self.dstfile=os.path.join(filepath,dstfilename)
       # mobj=TXTCreate(self.srcfile);
        #mobj.run();
        #mobj = TESTRun(self.srcfile,self.dstfile);
        #mobj.run();
        while True:
            LOG_PRINTF("Run Finish!!!\n\n\n")
            time.sleep(0.1)

    def log_thread(self):
        print('log_thread...')
        var = 1

        BUFSIZE = 1024
        reconcnt=0;
        port=qt.log.port
        ip_port=None
        while reconcnt <= qt.log.PORTCNT:
            try:
                rnd = random.randint(1, qt.log.PORTCNT)
                qt.log.port=port+rnd
                ip_port = (qt.log.ip, qt.log.port)
                print(ip_port)
                reconcnt = reconcnt+1;
                self.udp_server_client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                self.udp_server_client.bind(ip_port)

            except Exception as e:
                print(str(e))
                print("reconcnt : "+str(reconcnt));
                continue
            else:
                break

        if reconcnt > qt.log.PORTCNT:

            return ;
        logstr = "LOG service "+str(ip_port)+"  Init OK\n";
        self.textBrowser_log.append(logstr)
        self.textBrowser_log.moveCursor(self.textBrowser_log.textCursor().End);


        while self.log_thread_status == 1:
            msg, addr = self.udp_server_client.recvfrom(qt.log.BUFSIZE)
           # print(msg,addr)
            ret = str(msg, encoding="utf-8")
            print(ret)
            #udp_server_client.sendto(msg.upper(), addr)
            logstr=ret
            self.textBrowser_log.append(logstr)
            self.textBrowser_log.moveCursor(self.textBrowser_log.textCursor().End);
            time.sleep(0.1)


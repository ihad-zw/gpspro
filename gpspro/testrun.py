#!/usr/bin/env python
# -*- coding: utf-8 -*-

from log import LOG_PRINTF
class TESTRun:
    def __init__(self, srcfile,dstfile):
        self.srcfile=srcfile;
        self.dstfile=dstfile;

    def run(self):
        LOG_PRINTF(">>>run ")
        LOG_PRINTF("SRC: " + self.srcfile + "\n")
        LOG_PRINTF("DST: " + self.dstfile + "\n")
        dstfd = open(self.dstfile, 'wt', encoding='UTF-8')
        if dstfd == None:
            return;
        with open(self.srcfile, 'rt', encoding='UTF-8') as fd:
            for line in fd:
                print(line)
                '''
                ....
                
                '''

                dstfd.write(line + '\n')

        fd.close();
        dstfd.close();

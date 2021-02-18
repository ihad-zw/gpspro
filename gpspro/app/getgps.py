#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re
import os
import datetime;
import shutil
import logging
import traceback

from qt.log import LOG_PRINTF

class GetGPS:

    def __init__(self,q=None):
        self.q = q;
        self.rsrcfiles = None;
        self.rdstfiles = None;
        self.rdatatype = None;

    def run(self, srcfiles,dstfiles,datatype):
        self.rsrcfiles = srcfiles;
        self.rdstfiles = dstfiles;
        self.rdatatype = datatype;
        logging.info("srcfiles" + srcfiles);
        logging.info("dstfiles" + dstfiles);
        tmpfilesname = None;
        (filepath, tempfilename) = os.path.split(self.rsrcfiles);
        if len(filepath) > 0:
            tmpfilesname = tempfilename;
        else:
            tmpfilesname = "";

        now_time = datetime.datetime.now()
        time1_str = datetime.datetime.strftime(now_time, '%Y%m%dT%H%M%S')

        tmpfilesname = tmpfilesname + '_out_' + time1_str
        self.rdstfiles = os.path.join(self.rdstfiles, tmpfilesname)
        if  os.path.exists(self.rdstfiles):
            self.deletefiles(self.rdstfiles);
        if not os.path.exists(self.rdstfiles):
            os.makedirs(self.rdstfiles)

        LOG_PRINTF('SRC:' + self.rsrcfiles)
        LOG_PRINTF('DST:' + self.rdstfiles)
        files = os.listdir(self.rsrcfiles)
        for file in files:
            print("file: ",file)
            LOG_PRINTF("FILE: "+file)
            srcfile = os.path.join(self.rsrcfiles,file)
            (filepath, tempfilename) = os.path.split(srcfile);
            (shotname, extension) = os.path.splitext(tempfilename);
            dstfilename = shotname + '_out' + '.txt'
            dstfile = os.path.join(self.rdstfiles, dstfilename)
            self.gps_parse(srcfile,dstfile,datatype)


    def gps_parse(self,srcfile,dstfile,datatype):
        dstfd = open(dstfile, 'wt', encoding='UTF-8')
        if dstfd == None:
            return ;
        with open(srcfile, 'rt', encoding='UTF-8') as fd:
            for line in fd:
                line = line.strip('\n')
                #print(line);
                if datatype == "SS":
                    pass
                else:
                    mtype=re.findall(r"\$(.+?),",line,re.M)
                    #print(mtype[0])
                    if len(mtype) == 0 :
                        continue
                    if mtype[0]!="GNGGA" and mtype[0]!="GPGGA":
                        continue

               # print(line)
                #print(re.findall(r"[^ ]* [^,]*,[^,]*,(.+?),",line,re.M))
               # reg=re.compile(r'^[^ ]* (?P<mtype>.+?),(?P<time_str>.+?),(?P<latitude_str>.+?),(?P<lathem_str>.+?),(?P<longtitude_str>.+?),'
                #               r'(?P<longthem_str>.+?),[^,]*,[^,]*,[^,]*,(?P<altitude_str>.+?),(?P<altunit_str>.+?),')
                if datatype == "SS":
                    reg = re.compile(r'(?P<time_sec>.+?),(?P<time_nsec>.+?),(?P<mtype>.+?),(?P<time_str>.+?),(?P<latitude_str>.+?),(?P<lathem_str>.+?),(?P<longtitude_str>.+?),'
                        r'(?P<longthem_str>.+?),[^,]*,[^,]*,[^,]*,(?P<altitude_str>.+?),(?P<altunit_str>.+?),')
                else:
                    reg = re.compile(r'(?P<mtype>.+?),(?P<time_str>.+?),(?P<latitude_str>.+?),(?P<lathem_str>.+?),(?P<longtitude_str>.+?),'
                        r'(?P<longthem_str>.+?),[^,]*,[^,]*,[^,]*,(?P<altitude_str>.+?),(?P<altunit_str>.+?),')

                regMatch = reg.match(line)
                if regMatch == None :
                    print(line)
                    print("ERROR : regMatch == None")
                    continue
                linebits = regMatch.groupdict()
                print(linebits["latitude_str"],linebits["longtitude_str"])
                #for k, v in linebits.items():
                #    print(k + ": " + v)
                if (len(linebits["latitude_str"]) <= 7 or len(linebits["longtitude_str"]) <= 7):
                    continue;
                latitude=self.str2latitude(linebits["latitude_str"])
                longtitude=self.str2longtitude(linebits["longtitude_str"])

                strtmp=linebits["time_str"]+','+str(latitude)+','+linebits["lathem_str"]+','+str(longtitude)+','+linebits["longthem_str"]\
                      +','+linebits["altitude_str"]+','+linebits["altunit_str"]
                print(strtmp)
                dstfd.write(strtmp+'\n')

        fd.close();
        dstfd.close();


    def str2latitude(self,latitude_str):
        #print(latitude_str)
        degree=latitude_str[0:2]
        minute=latitude_str[2:]
        #print(degree+" "+minute)
        latitude=round(float(degree) + (float(minute) / 60),6)
       # print(latitude)
        return latitude

    def str2longtitude(self,longtitude_str):
        # print(longtitude_str)
        degree = longtitude_str[0:3]
        minute = longtitude_str[3:]
        # print(degree+" "+minute)
        longtitude = round(float(degree) + (float(minute) / 60),6)
        # print(longtitude)
        return longtitude




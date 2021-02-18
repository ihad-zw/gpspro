#!/usr/bin/env python
# -*- coding: utf-8 -*-

import socket

global ip
global port
global PORTCNT

ip='127.0.0.1'
port=19000

PORTCNT=100


BUFSIZE=1024
udp_server_client=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)

def LOG_PRINTF(str):
    msg=str;
    try:
        ip_port=(ip,port)
        print(ip_port)
        udp_server_client.sendto(msg.encode('utf-8'),ip_port)
    except Exception as e:
        print(str(e))
#    back_msg,addr=udp_server_client.recvfrom(BUFSIZE)
#    print(back_msg.decode('utf-8'),addr)
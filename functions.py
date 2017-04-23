#coding: utf-8
import time
import hashlib
import sys
import os
from socket import *

def create_udp_socket(ADDR) :
    try :
        sock = socket(AF_INET, SOCK_DGRAM)
        sock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        #print('Socket이 생성되었습니다.')
    except error as msg :
        print '소켓 생성 실패. Error Code : ',; print str(msg[0]),; print "Message ",; print str(msg[1])
        sys.exit()

    try :
        sock.bind(ADDR)
    except error as msg :
        print 'bind 실패 Error Code : ',; print str(msg[0]); print "Message ",; print str(msg[1])
        sys.exit()

    return sock

def create_tcp_socket(ADDR) :
    try :
        # SOCK_STREAM 연결지향(TCP/IP), SOCK_DGRAM 비연결지향(UDP)
        sock = socket(AF_INET, SOCK_STREAM)
        sock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        print('Socket이 생성되었습니다.')
    except error as msg :
        print '소켓 생성 실패. Error Code : ',; print str(msg[0]),; print "Message ",; print str(msg[1])
        sys.exit()

    return sock

def send_message(sock, message) :

    try :
        sock.send(message.encode('utf-8'))
    except :
        sock.send(message)

def receive_message(sock, size) :

    try :
        data = sock.recv(size)
        return data
    except  Exception as e :
        print(e)


def receive_file(sock, size) :
    return sock.recv(size)
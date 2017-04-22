# coding: utf-8
from socket import *
from functions import *
import os
import shutil
import sys


class UdpSocket:

    def __init__(self, PORT, BUFSIZE=1024 * 10, HOST=''):
        self.HOST = HOST
        self.PORT = PORT
        self.BUFSIZE = BUFSIZE
        self.ADDR = (HOST, PORT)

        try:
            self.sock = socket(AF_INET, SOCk_DGRAM)
            self.sock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        except Exception as e:
            print '소켓 생성 실패 : ', ; print e
            sys.exit()

        try:
            self.sock.bind(ADDR)
        except Exception as e:
            print 'bind 실패 : ', ; print e
            sys.exit()

    def receive_message(self) :
        data, addr = self.sock.recvfrom(self.BUFSIZE)
        try :
            data = data.decode('utf-8')
        except :
            pass
        return data, addr

    def send_message(self, addr, message) :
        try :
            message = message.encode('utf-8')
        except :
            pass
        self.sock.sendto(message, addr)
#coding: utf-8
import time
import hashlib
import sys
import os
from socket import *


class TcpSocket :

    def __init__(self, PORT, SERVER = None, LISTEN_NUMBER=15, BUFSIZE=1024 * 10, HOST=''):
        self.HOST = HOST
        self.PORT = PORT
        self.BUFSIZE = BUFSIZE
        self.ADDR = (HOST, PORT)


        try :
            # SOCK_STREAM 연결지향(TCP/IP), SOCK_DGRAM 비연결지향(UDP)
            self.sock = socket(AF_INET, SOCk_STREAM)
            self.sock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        except Exception as e :
            print '소켓 생성 실패 : ',; print e
            sys.exit()

        if SERVER is True :
            try :
                self.sock.bind(self.ADDR)
            except Exception as e :
                print 'bind 실패 : ',; print e

            try :
                self.sock.listen(LISTEN_NUMBER)
            except Exception as e :
                print 'LISTEN 실패 : ',; print e
                sys.exit()

    def send_message(self, message) :
        try :
            self.sock.send(message.encode('utf-8'))
        except :
            self.sock.send(message)

    def receive_message(self) :
        data = self.sock.recv(self.BUFSIZE)

        try :
            data = data.decode('utf-8')
        except :
            pass
        return data
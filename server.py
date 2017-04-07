#coding: utf-8
from socket import *
from server_thread import *
from pymongo import MongoClient
#from data_crawling import crawling_process

import signal
import sys

def create_tcp_socket() :
    try :
        sock = socket(AF_INET, SOCK_STREAM)
        sock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        print('Socket이 생성되었습니다.')
    except error as msg :
        print '소켓 생성 실패. Error Code : ',; print str(msg[0]),; print "Message ",; print str(msg[1])
        sys.exit()

    try :
        sock.bind(ADDR)
    except error as msg :
        print 'bind 실패 Error Code : ',; print str(msg[0]); print "Message "; print str(msg[1])
        sys.exit()

    try :
        sock.listen(LISTEN_NUMBER)

    except error as msg :
        print 'LISTEN 실패.'
        sys.exit()

    return sock

if __name__ == "__main__" :

    HOST = ""
    PORT = 5001
    ADDR = (HOST, PORT)
    LISTEN_NUMBER = 15

    tcpSock = create_tcp_socket()
    count = 0
    while (True) :
        try :
            print '연결 대기중...'
            (connection, (ip, port)) = tcpSock.accept()
            print "Connection ip : " + str(ip) + " Port : " + str(port)
            thread = Server_thread(ip, port, connection)
            thread.start()
        except Exception as e :
            print(e)

    tcpSock.close()
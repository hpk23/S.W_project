#coding: utf-8
from socket import *
from server_thread import *
from pymongo import MongoClient
#from data_crawling import crawling_process

import signal
import sys

def create_tcp_socket() :
    try :
        # SOCK_STREAM 연결지향(TCP/IP), SOCK_DGRAM 비연결지향(UDP)
        sock = socket(AF_INET, SOCK_STREAM) 
        sock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        print('Socket이 생성되었습니다.')
    except error as msg :
        print '소켓 생성 실패. Error Code : ',; print str(msg[0]),; print "Message ",; print str(msg[1])
        sys.exit()

    try :
        # 소켓에 ADDR변수의 주소를 할당해줌
        sock.bind(ADDR) 
    except error as msg :
        print 'bind 실패 Error Code : ',; print str(msg[0]),; print "Message ",; print str(msg[1])
        sys.exit()

    try :
        # socket을 통해 client의 접속 요청을 기다림 (LISTEN_NUMBER 만큼 받을 수 있음)
        sock.listen(LISTEN_NUMBER) 

    except error as msg :
        print 'LISTEN 실패.'
        sys.exit()

    return sock

if __name__ == "__main__" :

    HOST = ""
    PORT = 6001
    ADDR = (HOST, PORT)
    LISTEN_NUMBER = 15

    tcpSock = create_tcp_socket()
    while (True) :
        try :
            print '연결 대기중...'

            # 접속 요청한 client와 server의 접속을 받아들임
            (connection, (ip, port)) = tcpSock.accept() 
            print "Connection ip : " + str(ip) + " Port : " + str(port)

            # thread를 이용하여 client와 server를 통신 하도록 한 후 다시 accept로 돌아가 client의 연결을 기다림
            thread = Server_thread(ip, port, connection) 
            thread.start()
        except Exception as e :
            print(e)

    tcpSock.close()
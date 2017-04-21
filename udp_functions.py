#coding: utf-8
from socket import *
import os

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

def receive_message(sock, size) :
    data, addr = sock.recvfrom(size)
    try :
        data = data.decode('utf-8')
    except :
        pass
    return data, addr

def send_message(sock, addr, message) :
    try :
        message = message.encode('utf-8')
        sock.sendto(message, addr)
    except :
        sock.sendto(message, addr)
#coding: utf-8
from socket import *
csock = socket(AF_INET, SOCK_DGRAM)
csock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
csock.bind(('', 6001))
csock.sendto('2017 소개발 client', ('127.0.0.1',5001))
s, addr = csock.recvfrom(1024)
print s.decode('utf-8')
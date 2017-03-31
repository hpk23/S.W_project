#coding: utf-8
from socket import *
svrsock = socket(AF_INET, SOCK_DGRAM)
svrsock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
svrsock.bind(('', 5001))
s, addr = svrsock.recvfrom(1024)
print s.decode('utf-8')
svrsock.sendto('2017 소개발 server',addr)
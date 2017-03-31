#coding: utf-8
from socket import *

if __name__ == "__main__" :

    HOST = ''
    PORT = 5001
    ADDR = (HOST, PORT)
    BUFSIZE = 1024 * 10

    udpSock = socket(AF_INET, SOCK_DGRAM)
    udpSock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    udpSock.bind(ADDR)
    CLIENT_NAME, CLIENT_ADDR = udpSock.recvfrom(BUFSIZE)
    udpSock.sendto('3 TEAM SERVER', CLIENT_ADDR)

    file_name = ''
    file = open('D:/2017_S.W/' + file_name.decode('utf-8'), 'rb')

    print 'send to ' + CLIENT_NAME
    for line in file :
        udpSock.sendto(line, CLIENT_ADDR)
    udpSock.sendto('EOF', CLIENT_ADDR)


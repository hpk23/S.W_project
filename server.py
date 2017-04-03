#coding: utf-8
from socket import *
import os

if __name__ == "__main__" :

    HOST = ''
    PORT = 5001
    ADDR = (HOST, PORT)
    BUFSIZE = 1024 * 10

    file_name = '릴렉스-힘내.mp3'.decode('utf-8')

    user_input = 'Y'
    file_size = os.path.getsize('D:/2017_S.W/' + file_name)

    while user_input == 'Y' or user_input == 'y' :

        udpSock = socket(AF_INET, SOCK_DGRAM)
        udpSock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        udpSock.bind(ADDR)
        CLIENT_NAME, CLIENT_ADDR = udpSock.recvfrom(BUFSIZE)
        udpSock.sendto('3 TEAM SERVER', CLIENT_ADDR)
        print 'send to ' + CLIENT_NAME

        file = open('D:/2017_S.W/' + file_name, 'rb')

        for line in file :
            udpSock.sendto(line, CLIENT_ADDR)
        udpSock.sendto('EOF', CLIENT_ADDR)
        udpSock.sendto(str(file_size), CLIENT_ADDR)
        user_input, user_addr = udpSock.recvfrom(BUFSIZE)
        print user_input

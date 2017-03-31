#coding: utf-8
from socket import *

if __name__ == "__main__" :

    HOST = ''
    PORT = 6001
    ADDR = (HOST, PORT)
    BUFSIZE = 1024 * 10

    SERVER_HOST = '127.0.0.1'
    SERVER_PORT = 5001
    SERVER_ADDR = (SERVER_HOST, SERVER_PORT)

    csock = socket(AF_INET, SOCK_DGRAM)
    csock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    csock.bind(ADDR)

    MYNAME = raw_input('이름을 입력해주세요 : ')

    csock.sendto(MYNAME, SERVER_ADDR)
    s, addr = csock.recvfrom(BUFSIZE)

    recv_file = open('temp.mp3', 'wb')
    s, addr = csock.recvfrom(BUFSIZE)
    while s != 'EOF' :
        recv_file.write(s)
        s, addr = csock.recvfrom(BUFSIZE)

    #s, addr = csock.recvfrom(BUFSIZE)
    #print s.decode('utf-8')
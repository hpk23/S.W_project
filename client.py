#coding: utf-8
from socket import *
import os
import re
import io

if __name__ == "__main__" :

    os.system('chcp 949') # cmd창에서 한글이 보이지 않는 현상 해결
    os.system('cls')

    HOST = ''
    PORT = 6001
    ADDR = (HOST, PORT)
    BUFSIZE = 1024


    SERVER_HOST = '210.117.182.122'
    SERVER_PORT = 5001
    SERVER_ADDR = (SERVER_HOST, SERVER_PORT)

    csock = socket(AF_INET, SOCK_DGRAM)
    csock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    csock.bind(ADDR)

    MYNAME = input("이름을 입력해주세요 : ").encode('utf-8')

    csock.sendto(MYNAME, SERVER_ADDR)
    reply, server_addr = csock.recvfrom(BUFSIZE) # server로 부터 접속 응답 받음
    print (reply.decode('utf-8'))

    s, server_addr = csock.recvfrom(BUFSIZE)
    s = s.decode('utf-8')
    while(s != "LIST END") :
        print (s)
        s, server_addr = csock.recvfrom(BUFSIZE)
        s = s.decode('utf-8')
    number = input("번호를 입력 해주세요 : ").encode('utf-8')
    csock.sendto(number, SERVER_ADDR)

    s, addr = csock.recvfrom(BUFSIZE)
    out_file = io.open("temp.mp3", "wb")
    while repr(s).find("EOF") == -1 :
        out_file.write(s)
        s, addr = csock.recvfrom(BUFSIZE)
    print (s)
    out_file.close()
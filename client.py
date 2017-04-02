#coding: utf-8
from socket import *
import os

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

    comment = '이름을 입력해주세요 : '.decode('utf-8')
    print comment,
    MYNAME = raw_input() # raw_input에는 한글이 왜 적용 안되지..?

    #csock.sendto(MYNAME, SERVER_ADDR)

    s, server_addr = csock.recvfrom(BUFSIZE) # server로 부터 접속 응답 받음

    file_line, server_addr = csock.recvfrom(BUFSIZE)
    while(1) :
        csock.sendto(MYNAME, SERVER_ADDR)
        recv_file = open('temp.mp3', 'wb')
        while file_line != 'EOF' :
            recv_file.write(file_line)
            file_line, server_addr = csock.recvfrom(BUFSIZE)

        recv_file_size = os.path.getsize('D:/2017_S.W/S.W_project/' + 'temp.mp3')
        file_size, server_addr = csock.recvfrom(BUFSIZE)
        print file_size, " :: ", recv_file_size
        if file_size != str(recv_file_size) :
            print "전송중에 파일이 손상 되었습니다. 다시 받으시겠습니까? : ".decode('utf-8'),
            my_input = raw_input()
            csock.sendto(my_input, SERVER_ADDR)
            if my_input != 'Y' or my_input != 'y' : break

        else :
            csock.sendto('N', SERVER_ADDR)

#coding: utf-8
from socket import *
from UDP_CLASS import *
from TCP_CLASS import *
import os
import shutil
import sys



if __name__ == "__main__" :

    HOST = ''
    PORT = 5006
    ADDR = (HOST, PORT)
    BUFSIZE = 1024

    SERVER_HOST = '210.117.182.122'
    SERVER_PORT = 5005
    SERVER_ADDR = (SERVER_HOST, SERVER_PORT)

    connection = UdpSocket(PORT, BUFSIZE=BUFSIZE)
    connection.send_message(SERVER_ADDR, "hello")

    music_list, addr = connection.receive_message()
    print music_list

    print "전송받을 파일의 번호를 입력해주세요( 디렉토리로 전송받기 : 0) : ",

    number = input()

    connection.send_message(addr, str(number))  # 선택한 번호를 서버에 전송

    file_size, addr = connection.receive_message() # 내가 받고자 하는 파일의 크기

    if int(file_size) > 1024*64 :
        connection = TcpSocket(PORT, BUFSIZE=BUFSIZE)
        #time.sleep(1)
        connection.sock.connect(SERVER_ADDR)

        if number is 0:
            connection.receive_directory()
        else:
            file_name = connection.receive_message()
            file_name = file_name.split('/')[-1]

            connection.receive_file(file_name)
        sys.exit(0)

    connection.sock.settimeout(3)
    if number is 0 :
        connection.receive_directory()
    else :
        file_name, addr = connection.receive_message()
        connection.receive_file(file_name)
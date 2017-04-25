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
    BUFSIZE = 1024 * 30

    SERVER_HOST = '210.117.182.122'
    SERVER_PORT = 5005
    SERVER_ADDR = (SERVER_HOST, SERVER_PORT)

    protocol = -1

    while True :
        print "TCP : 0\tUDP : 1\n전송 프로토콜 선택 : ",
        protocol = input()
        if not (protocol is 0 or protocol is 1) :
            print "\n잘못 선택 하셨습니다 0 또는 1의 숫자를 입력해주세요"
            continue
        else :
            break

    connection = UdpSocket(PORT, BUFSIZE=BUFSIZE)
    connection.send_message(SERVER_ADDR, str(protocol))  # 선택한 프로토콜을 서버에 전송

    if protocol is 0 :
        connection = TcpSocket(PORT, BUFSIZE=BUFSIZE)
        time.sleep(1)
        connection.sock.connect(SERVER_ADDR)

        reply = connection.receive_message()  # 서버로부터 응답 메시지 받기
        print reply

        music_list = connection.receive_message()  # 서버로부터 음악리스트 전송 받기
        print music_list

        print "전송받을 파일의 번호를 입력해주세요( 디렉토리로 전송받기 : 0) : ",
        number = input()
        connection.send_message(str(number))  # 선택한 번호를 서버에 전송

        connection.sock.settimeout(3)

        if number is 0:
            connection.receive_directory()
        else :
            file_name = connection.receive_message()
            connection.receive_file(file_name)
        sys.exit(0)

    reply, addr = connection.receive_message() # 서버로부터 응답 메시지 받기
    print reply
    time.sleep(1)

    music_list, addr = connection.receive_message() # 서버로부터 음악리스트 전송 받기
    print music_list

    print "전송받을 파일의 번호를 입력해주세요( 디렉토리로 전송받기 : 0) : ",
    number = input()
    connection.send_message(SERVER_ADDR, str(number)) # 선택한 번호를 서버에 전송

    connection.sock.settimeout(3)

    if number is 0 :
        connection.receive_directory()
    else :
        file_name, addr = connection.receive_message()
        connection.receive_file(file_name)
#coding: utf-8
from socket import *
from UDP_CLASS import *
from TCP_CLASS import *
import os
import shutil
import sys


if __name__ == "__main__" :

    HOST = ''
    PORT = 7050
    ADDR = (HOST, PORT)
    BUFSIZE = 1024

    SERVER_HOST = '210.117.182.122'
    SERVER_PORT = 6050
    SERVER_ADDR = (SERVER_HOST, SERVER_PORT)

    connection = UdpSocket(PORT, BUFSIZE=BUFSIZE)
    connection.send_message(SERVER_ADDR, "hello")

    music_list, addr = connection.receive_message()
    print music_list

    print "전송받을 파일의 번호를 입력해주세요( 디렉토리로 전송받기 : 0) : ",

    number = input()

    connection.send_message(addr, str(number))  # 선택한 번호를 서버에 전송



    if number is 0 :
        length, addr = connection.receive_message()
        length = int(length)
        strange_files = []

        for i in range(length) :
            file_name, addr = connection.receive_message()
            print "file_name : ",; print file_name
            file_size, addr = connection.receive_message()
            file_size = int(file_size)
            directory_name = '/'.join(file_name.split('/')[:-1])

            if not os.path.exists(directory_name) :
                os.mkdir(directory_name)

            if file_size > 1024 * 64 :
                if connection.protocol != "TCP" :
                    connection.sock.shutdown(1)
                    del connection
                    connection = TcpSocket(PORT, BUFSIZE=BUFSIZE)
                    connection.sock.connect(SERVER_ADDR)

                check, file_info = connection.receive_file(file_name, True)

                if check == False :
                    strange_files.append(file_info)

            else :
                check, file_info = connection.receive_file(addr, file_name, True)
                if check == False :
                    strange_files.append(file_info)

            if connection.protocol != "UDP" :
                del connection
                connection = UdpSocket(PORT, BUFSIZE=BUFSIZE)

        for file_name, original_hash_value, receive_hash_value, original_file_size, receive_file_size in strange_files:
            print file_name, ;
            print "\n\n파일의 해시값이 다릅니다."
            print "원본 파일 크기 : " + str(original_file_size) + " bytes\t받은 파일 크기 : " + str(receive_file_size) + " bytes"
            print "원본 파일 해시값 : " + str(original_hash_value) + " 받은 파일 해시값 : " + str(receive_hash_value)
            while (True):
                print "파일을 지우시겠습니까?(Y/N) : ",
                user_input = raw_input()
                if user_input.upper() != 'Y' and user_input.upper() != 'N':
                    print "잘못 입력 하셨습니다.\n"
                    continue
                elif user_input.upper() == 'Y':
                    os.remove(file_name)
                    print("파일 삭제 완료")
                break

    else :
        file_size, addr = connection.receive_message()  # 내가 받고자 하는 파일의 크기

        if int(file_size) > 1024*64 :

            del connection
            connection = TcpSocket(PORT, BUFSIZE=BUFSIZE)
            connection.sock.connect(SERVER_ADDR)

            file_name = connection.receive_message()
            file_name = file_name.split('/')[-1]

            connection.receive_file(file_name)
            sys.exit(0)

        else :
            connection.sock.settimeout(3)

            file_name, addr = connection.receive_message()
            file_name = file_name.split('/')[-1]
            connection.receive_file(addr, file_name)
#coding: utf-8
import time
import hashlib
import sys
import os
import datetime
from socket import *
import socket as sk
from pymongo import MongoClient


class TcpSocket :

    def __init__(self, PORT, SERVER = None, LISTEN_NUMBER=15, BUFSIZE=1024 * 50, HOST='') :
        self.HOST = HOST
        self.PORT = PORT
        self.BUFSIZE = BUFSIZE
        self.ADDR = (HOST, PORT)
        MONGO_ADDR = "127.0.0.1:27017"
        connection = MongoClient(MONGO_ADDR)
        self.db = connection.music_db
        self.collection = self.db.music_list
        self.protocol = "TCP"


        try :
            # SOCK_STREAM 연결지향(TCP/IP), SOCK_DGRAM 비연결지향(UDP)
            self.sock = socket(AF_INET, SOCK_STREAM)
            self.sock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)

        except Exception as e :
            print '소켓 생성 실패 : ',; print e
            sys.exit(1)

        if SERVER is True :
            try :
                self.sock.bind(self.ADDR)
            except Exception as e :
                print 'bind 실패 : ',; print e

            try :
                self.sock.listen(LISTEN_NUMBER)
            except Exception as e :
                print 'LISTEN 실패 : ',; print e
                sys.exit(1)

            self.accept_sock = self.sock

    def setClient(self, client_sock, client_address) :
        self.sock = client_sock
        self.client_ADDR = client_address

    def __del__(self) :
        self.sock.close()

    def receive_message(self):
        while True :
            data = self.sock.recv(self.BUFSIZE)
            if not data : return ''
            try :
                data = data.decode('utf-8')
            except :
                pass
            self.sock.send("receive data")
            return data

    def send_message(self, message) :
        try :
            sent = self.sock.send(message.encode('utf-8'))
        except :
            self.sock.send(message)
        data = self.sock.recv(self.BUFSIZE)
        while data != "receive data" :
            data = self.sock.recv(self.BUFSIZE)

    def send_file(self, file_name) :

        print 'start send_file'

        hasher = hashlib.sha224()

        reply = self.receive_message() # 파일 존재 여부에 대한 메시지 받기 ( None : 없음, Exist : 존재 )
        file = open(file_name, "rb")

        if reply == "Exist" :

            jump_size = self.receive_message() # 클라이언트에 존재하던 파일의 크기를 받음
            jump_size = int(jump_size)
            my_hash_value = self.get_hash_value(file_name, jump_size)
            self.send_message(str(my_hash_value)) # 무결성 체크를 위해 클라이언트에게 해쉬값 전송
            buf = file.read(jump_size) # jump_size 만큼 파일 포인터 점프
            hasher.update(buf)

            file_size = os.path.getsize(file_name)
            float_number = round(( float(file_size) - jump_size) / float(self.BUFSIZE) + 0.49999999, 0)
            length = int(float_number)
            self.send_message(str(length))

        else :

            file_size = os.path.getsize(file_name)
            float_number = round( float(file_size) / float(self.BUFSIZE) + 0.49999999, 0)
            length = int(float_number)
            self.send_message(str(length))
        try:
            print file_name.split('/')[-1].decode('cp949').encode('utf-8'),; print '을 전송합니다.'
        except:
            print file_name.split('/')[-1],; print '을 전송합니다.'


        buf = file.read(self.BUFSIZE)
        while buf :
            hasher.update(buf)
            self.send_message(buf)
            buf = file.read(self.BUFSIZE)

        self.send_message(str(file_size))
        self.send_message(str(hasher.hexdigest()))
        try :
            print file_name.split('/')[-1].decode('cp949').encode('utf-8'),; print '전송완료\n'
        except :
            print file_name.split('/')[-1],; print '전송완료\n'

    def send_directory(self, directory_path) :
        current_path = directory_path.split('/')[-1]
        directory = directory_path.split('/')[-1]

        length = 0
        for path, dirs, files in os.walk(directory_path) :
            for file in files :
                length += 1

        self.send_message(str(length))

        for path, dirs, files in os.walk(directory_path):
            for file in files:
                current_directory = path.replace('\\', '/').split('/')[-1]
                if directory != current_directory:
                    directory = current_directory
                    current_path = current_path + '/' + directory
                file_name = current_path + '/' + file
                self.send_message(file_name)  # file_name 전송

                send_file_name = path + '/' + file
                self.send_file(send_file_name)

    def receive_directory(self) :
        length = int(self.receive_message())
        strange_files = []

        for i in range(length) :
            file_name = self.receive_message()
            directory_name = '/'.join(file_name.split('/')[:-1])

            if not os.path.exists(directory_name) :
                os.mkdir(directory_name)

            #check, file_info = self.receive_file(file_name, directory=True)


            check, file_info = self.receive_file(file_name, True)

            if check == False:
                strange_files.append(file_info)

        for file_name, original_hash_value, receive_hash_value, original_file_size, receive_file_size in strange_files :
            print file_name,; print "\n\n파일의 해시값이 다릅니다."
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


    def get_hash_value(self, file_name, file_size = None) :

        if file_size is None :
            file_size = os.path.getsize(file_name)

        try :
            hasher = hashlib.sha224()

            with open(file_name, "rb") as file:
                for i in range(0, file_size, self.BUFSIZE) :
                    size = min(file_size - i, self.BUFSIZE)
                    if size < 0 : size = 0
                    buf = file.read(size)
                    if buf : hasher.update(buf)
            return hasher.hexdigest()
        except Exception, e :
            print e
            sys.exit(-1)

    def receive_file(self, file_name, directory = None) :

        start = datetime.datetime.now()

        if os.path.exists(file_name) :

            self.send_message("Exist") # 파일 존재 여부 확인 메시지 보내기

            out_file = open(file_name, 'ab')

            file_size = os.path.getsize(file_name)
            self.send_message(str(file_size)) # 서버로 내가 가지고있던 파일 크기를 보냄 ( 서버에서는 size 만큼 파일 포인터 점프 )

            ## 존재하던 파일의 무결성 체크 ##
            my_hash_value = self.get_hash_value(file_name, file_size)
            recv_hash_value = self.receive_message()

            if str(my_hash_value) != str(recv_hash_value) :
                print "존재하던 파일이 손상 되었습니다. 삭제한 후에 다시 시도해주세요!"
                return

            print "파일 이어받기를 시작합니다."
            length = self.receive_message()
            length = int(length)
            for i in range(length) :
                data = self.receive_message()
                while not data :
                    data = self.receive_message()
                out_file.write(data)
            out_file.close()

        else :
            self.send_message("None")  # 파일 존재 여부 확인 메시지 보내기
            out_file = open(file_name, "wb")
            length = int(self.receive_message())

            for i in range(length) :
                data = self.receive_message()
                while not data :
                    data = self.receive_message()
                out_file.write(data)
            out_file.close()

        end = datetime.datetime.now()
        time.sleep(2)
        original_file_size = self.receive_message()
        original_hash_value = self.receive_message()

        hasher = hashlib.sha224()

        receive_file_size = os.path.getsize(file_name)
        with open(file_name, "rb") as receive_file:
            buf = receive_file.read(self.BUFSIZE)
            while buf:
                hasher.update(buf)
                buf = receive_file.read(self.BUFSIZE)

        receive_hash_value = hasher.hexdigest()
        if str(original_hash_value) == str(receive_hash_value):
            try:
                print file_name.split('/')[-1].decode('cp949').encode('utf-8') + " 전송완료"
            except:
                print file_name.split('/')[-1].encode('utf-8') + " 전송완료"
            print str(round(float(receive_file_size / (1024 * 1024) + 1.0) / ((end - start).seconds + 1.0), 2)) + " Mb/sec"
            return (True, file_name)

        else:
            try:
                print file_name.split('/')[-1].decode('cp949').encode('utf-8') + " 전송완료"
            except:
                print file_name.split('/')[-1].encode('utf-8') + " 전송완료"
            if directory is None:
                print "파일의 해시값이 다릅니다."
                print "원본 파일 해시값 : " + str(original_hash_value) + " 받은 파일 해시값 : " + str(receive_hash_value)
                print "원본 파일 크기 : " + str(original_file_size) + " bytes\t받은 파일 크기 : " + str(receive_file_size) + " bytes"
                while (True):
                    print "파일을 지우시겠습니까?(Y/N) : ",
                    user_input = raw_input()
                    if user_input.upper() != 'Y' and user_input.upper() != 'N':
                        print "잘못 입력 하셨습니다.\n"
                        continue

                    elif user_input.upper() == 'Y':
                        os.remove(file_name)
                        print("파일 삭제 완료")
            print str(round(float(receive_file_size / (1024 * 1024) + 1.0) / ((end - start).seconds + 1.0), 2)) + " Mb/sec"
            return (False, [file_name, original_hash_value, receive_hash_value, original_file_size, receive_file_size])

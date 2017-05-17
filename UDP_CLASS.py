# coding: utf-8
from socket import *
from pymongo import MongoClient
import socket as sk
import os
import sys
import hashlib
import datetime


class UdpSocket:

    def __init__(self, PORT, BUFSIZE=1024 * 50, HOST='') :
        self.HOST = HOST
        self.PORT = PORT
        self.BUFSIZE = BUFSIZE
        self.ADDR = (HOST, PORT)
        MONGO_ADDR = "127.0.0.1:27017"
        connection = MongoClient(MONGO_ADDR)
        self.db = connection.music_db
        self.collection = self.db.music_list
        self.protocol = "UDP"

    def setSocket(self) :
        try :
            self.sock.close()
        except Exception, e :
            pass
        try :
            self.sock = socket(AF_INET, SOCK_DGRAM)
            self.sock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)

        except Exception as e:
            print '소켓 생성 실패 : ',; print e
            sys.exit()

        try:
            self.sock.bind(self.ADDR)
        except Exception as e:
            print 'bind 실패 : ',; print e
            sys.exit()

    def __del__(self) :
        self.sock.close()

    def receive_message(self) :
        while True :
            data, addr = self.sock.recvfrom(self.BUFSIZE)
            if not data : return None, None
            try :
                data = data.decode('utf-8')
            except :
                pass
            self.sock.sendto("receive data", addr)
            return data, addr

    def send_message(self, addr, message) :
        try :
            self.sock.sendto(message.encode('utf-8'), addr)
        except :
            self.sock.sendto(message, addr)
        data, addr = self.sock.recvfrom(self.BUFSIZE)
        while data != "receive data" :
            data, addr = self.sock.recvfrom(self.BUFSIZE)


    def receive_directory(self) :
        length, addr = self.receive_message()
        length = int(length)
        strange_files = []
        for i in range(length) :
            file_name, addr = self.receive_message() # 파일 이름 전송 받기

            directory = '/'.join(file_name.split('/')[:-1])
            try :
                if not os.path.isdir(directory) :
                    os.mkdir(directory)
            except :
                pass

            check, file_info = self.receive_file(file_name, True)
            if check == False :
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


    def send_directory(self, addr, directory_path) :
        current_path = directory_path.split('/')[-1]
        directory = directory_path.split('/')[-1]

        length = 0
        for path, dirs, files in os.walk(directory_path) :
            for file in files :
                length += 1
        self.send_message(addr, str(length))
        for path, dirs, files in os.walk(directory_path) :
            for file in files :
                current_directory = path.replace('\\', '/').split('/')[-1]
                if directory != current_directory :
                    directory = current_directory
                    current_path = current_path + '/' + directory

                file_name = current_path + '/' + file
                self.send_message(addr, file_name) # file_name 전송
                send_file_name = path + '/' + file
                try :
                    send_file_name = send_file_name.decode('utf-8')
                except :
                    pass
                self.send_file(addr, send_file_name)

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

    def receive_file(self, addr, file_name, directory=None) :

        start = datetime.datetime.now()

        if os.path.exists(file_name) :
            self.send_message(addr, "Exist") # 파일 존재 여부 확인 메시지 보내기


            out_file = open(file_name, 'ab')

            file_size = os.path.getsize(file_name)
            self.send_message(addr, str(file_size))

            ## 존재하던 파일의 무결성 체크 ##
            my_hash_value = self.get_hash_value(file_name, file_size)
            recv_hash_value, addr = self.receive_message()

            if str(my_hash_value) != str(recv_hash_value) :
                print "존재하던 파일이 손상 되었습니다. 삭제한 후에 다시 시도해주세요!"
                return

            print "파일 이어받기를 시작합니다."
            length, addr = self.receive_message()
            length = int(length)
            print "length : ",; print length
            for i in range(length):
                data, addr = self.receive_message()
                while not data:
                    data, addr = self.receive_message()
                out_file.write(data)
            out_file.close()

        else :
            print 'None~'
            self.send_message(addr, "None")
            print 'send  None end'
            out_file = open(file_name, "wb")
            length, addr = self.receive_message()
            print 'receive length'
            length = int(length)

            for i in range(length) :
                data, addr = self.receive_message()
                while not data :
                    data, addr = self.receive_message()
                out_file.write(data)
            out_file.close()

        end = datetime.datetime.now()


        original_file_size, addr = self.receive_message()
        original_hash_value, addr = self.receive_message()

        hasher = hashlib.sha224()

        receive_file_size = os.path.getsize(file_name)


        with open(file_name, "rb") as receive_file:
            buf = receive_file.read(self.BUFSIZE)
            while buf:
                hasher.update(buf)
                buf = receive_file.read(self.BUFSIZE)

        receive_hash_value = hasher.hexdigest()
        if str(original_hash_value) == str(receive_hash_value) :
            try :
                print file_name.split('/')[-1].decode('cp949').encode('utf-8') + " 전송완료"
            except :
                print file_name.split('/')[-1].encode('utf-8') + " 전송완료"

            #print "원본 파일 크기 : " + str(original_file_size) + " bytes\t받은 파일 크기 : " + str(receive_file_size) + " bytes"
            #print "원본 파일 해시값 : " + str(original_hash_value) + " 받은 파일 해시값 : " + str(receive_hash_value)
            print str(round(float(receive_file_size / (1024 * 1024) + 1.0) / ((end - start).seconds + 1.0), 2)) + " Mb/sec"
            return (True, file_name)
        else:
            try :
                print file_name.split('/')[-1].decode('cp949').encode('utf-8') + " 전송완료"
            except :
                print file_name.split('/')[-1].encode('utf-8') + " 전송완료"

            if directory is None :
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


    def send_file(self, addr, file_name) :

        hasher = hashlib.sha224()

        reply, addr = self.receive_message()
        file = open(file_name, "rb")

        if reply == "Exist" :

            jump_size, addr = self.receive_message()
            jump_size = int(jump_size)
            my_hash_value = self.get_hash_value(file_name, jump_size)
            self.send_message(addr, str(my_hash_value))
            buf = file.read(jump_size)
            hasher.update(buf)

            file_size = os.path.getsize(file_name)
            float_number = round((float(file_size) - jump_size) / float(self.BUFSIZE) + 0.49999999, 0)
            length = int(float_number)
            self.send_message(addr, str(length))

        else :
            file_size = os.path.getsize(file_name)
            float_number = round(float(file_size) / float(self.BUFSIZE) + 0.49999999, 0)
            length = int(float_number)
            self.send_message(addr, str(length))

        try :
            print file_name.split('/')[-1].decode('cp949').encode('utf-8'),; print '을 전송합니다.'
        except :
            print file_name.split('/')[-1],; print '을 전송합니다.'

        buf = file.read(self.BUFSIZE)
        while buf:
            hasher.update(buf)
            self.send_message(addr, buf)
            buf = file.read(self.BUFSIZE)

        self.send_message(addr, str(file_size)) # file size 전송
        self.send_message(addr, str(hasher.hexdigest())) # file hash value 전송

        try :
            print file_name.split('/')[-1].decode('cp949').encode('utf-8'),; print '전송완료\n'
        except :
            print file_name.split('/')[-1],; print '전송완료\n'



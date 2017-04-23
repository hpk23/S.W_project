# coding: utf-8
from socket import *
from pymongo import MongoClient
import os
import sys
import hashlib


class UdpSocket:

    def __init__(self, PORT, BUFSIZE=1024 * 10, HOST=''):
        self.HOST = HOST
        self.PORT = PORT
        self.BUFSIZE = BUFSIZE
        self.ADDR = (HOST, PORT)
        MONGO_ADDR = "127.0.0.1:27017"
        connection = MongoClient(MONGO_ADDR)
        self.db = connection.music_db
        self.collection = self.db.music_list

        try:
            self.sock = socket(AF_INET, SOCK_DGRAM)
            self.sock.setsockopt(SOL_SOCKET, SO_SNDBUF, self.BUFSIZE)
            #self.sock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)

        except Exception as e:
            print '소켓 생성 실패 : ', ; print e
            sys.exit()

        try:
            self.sock.bind(self.ADDR)
        except Exception as e:
            print 'bind 실패 : ', ; print e
            sys.exit()




    def __del__(self) :
        self.sock.close()


    def receive_message(self) :

        try :
            data, addr = self.sock.recvfrom(self.BUFSIZE)
            try :
                data = data.decode('utf-8')
            except :
                pass
            self.sock.sendto("receive data", addr)
            return data, addr
        except Exception as e :
            return ('', '')



    def send_message(self, addr, message) :

        try :
            try :
                message = message.encode('utf-8')
            except :
                pass
            self.sock.sendto(message, addr)
            reply, addr = self.sock.recvfrom(self.BUFSIZE)
        except Exception as e :
            pass





    def receive_directory(self) :
        length, addr = self.receive_message()
        length = int(length)
        for i in range(length) :
            file_name, addr = self.receive_message() # 파일 이름 전송 받기

            directory = '/'.join(file_name.split('/')[:-1])
            print 'file_name : ',; print file_name,; print ' --> ',; print directory
            if not os.path.isdir(directory) :
                os.mkdir(directory)

            self.receive_file(file_name)


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
                print send_file_name
                try :
                    send_file_name = send_file_name.decode('utf-8')
                except :
                    pass
                self.send_file(addr, send_file_name)



    def receive_file(self, file_name) :
        with open(file_name, "wb") as out_file :
            length, addr = self.receive_message()
            length = int(length)

            for i in range(length) :
                data, addr = self.receive_message()
                out_file.write(data)
        out_file.close()

    def send_file(self, addr, file_name) :

        hasher = hashlib.sha224()
        file_size = os.path.getsize(file_name)

        total = int((file_size) / self.BUFSIZE + 0.5) + 1
        self.send_message(addr, str(total))
        count = 0
        with open(file_name, "rb") as f:
            buf = f.read(self.BUFSIZE)
            while buf :
                count += 1
                hasher.update(buf)
                self.send_message(addr, buf)
                buf = f.read(self.BUFSIZE)
        print count
        print 'complete send file'
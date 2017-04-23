#coding: utf-8
import time
import hashlib
import sys
import os
from socket import *
from pymongo import MongoClient


class TcpSocket :

    def __init__(self, PORT, SERVER = None, LISTEN_NUMBER=15, BUFSIZE=1024 * 50, HOST=''):
        self.HOST = HOST
        self.PORT = PORT
        self.BUFSIZE = BUFSIZE
        self.ADDR = (HOST, PORT)
        MONGO_ADDR = "127.0.0.1:27017"
        connection = MongoClient(MONGO_ADDR)
        self.db = connection.music_db
        self.collection = self.db.music_list

        try :
            # SOCK_STREAM 연결지향(TCP/IP), SOCK_DGRAM 비연결지향(UDP)
            self.sock = socket(AF_INET, SOCK_STREAM)
            self.sock.setsockopt(SOL_SOCKET, SO_SNDBUF, self.BUFSIZE)
            #self.sock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)

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

    def setClient(self, client_sock, client_address):
        self.sock = client_sock
        self.client_ADDR = client_address

    #def __del__(self) :
    #    self.sock.close()

    def send_message(self, message) :
        try :
            self.sock.send(message.encode('utf-8'))
        except :
            self.sock.send(message)
        self.sock.recv(self.BUFSIZE)

    def receive_message(self) :
        data = self.sock.recv(self.BUFSIZE)
        try :
            data = data.decode('utf-8')
        except :
            pass
        self.sock.send("receive data")
        return data


    def receive_directory(self) :
        length = self.receive_message()
        length = int(length)
        for i in range(length) :
            file_name = self.receive_message() # 파일 이름 전송 받기

            directory = '/'.join(file_name.split('/')[:-1])
            print 'file_name : ',; print file_name,; print ' --> ',; print directory
            if not os.path.isdir(directory) :
                os.mkdir(directory)

            self.receive_file(file_name)


    def send_directory(self, directory_path) :
        current_path = directory_path.split('/')[-1]
        directory = directory_path.split('/')[-1]

        length = 0
        for path, dirs, files in os.walk(directory_path) :
            for file in files :
                length += 1
        self.send_message(str(length))
        for path, dirs, files in os.walk(directory_path) :
            for file in files :
                current_directory = path.replace('\\', '/').split('/')[-1]
                if directory != current_directory :
                    directory = current_directory
                    current_path = current_path + '/' + directory

                file_name = current_path + '/' + file
                self.send_message(file_name) # file_name 전송
                send_file_name = path + '/' + file
                print send_file_name
                try :
                    send_file_name = send_file_name.decode('utf-8')
                except :
                    pass
                self.send_file(send_file_name)



    def receive_file(self, file_name) :
        with open(file_name, "wb") as out_file :
            length = self.receive_message()
            length = int(length)

            for i in range(length) :
                data = self.receive_message()
                out_file.write(data)
        out_file.close()

    def send_file(self, file_name) :

        hasher = hashlib.sha224()
        file_size = os.path.getsize(file_name)

        total = int((file_size) / self.BUFSIZE + 0.5) + 1
        self.send_message(str(total))
        count = 0
        with open(file_name, "rb") as f:
            buf = f.read(self.BUFSIZE)
            while buf :
                count += 1
                hasher.update(buf)
                self.send_message(buf)
                buf = f.read(self.BUFSIZE)
        print count
        print 'complete send file'
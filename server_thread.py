#coding: utf-8


from pymongo import MongoClient
from TCP_CLASS import *
import threading


class ServerThread(threading.Thread) : # threading.Thread 클래스를 상속 받음

    # __init__ 함수는 C++ 클래스의 생성자와 같은 역할을 한다.
    # self 는 C++의 this 와 같은 역할
    def __init__(self, connection, file_name, file_size, number) :
        super(ServerThread, self).__init__()
        self._stop = threading.Event()
        self.connection = connection
        self.file_name = file_name
        self.file_size = file_size
        self.number = number


    def stop(self):
        self._stop.set()

    def stopped(self):
        return self._stop.isSet()

    def __del__(self) :
        self.stop()
        #self.join()

    def run(self) :

        self.connection.sock.settimeout(10)

        directory_path = "D:/2017_S.W/1st"
        if self.number is 0:
            self.connection.send_directory(directory_path)

        else:
            self.connection.send_file(self.file_name)

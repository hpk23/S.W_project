#coding: utf-8


from pymongo import MongoClient
from TCP_CLASS import *
import threading


class ServerThread(threading.Thread) : # threading.Thread 클래스를 상속 받음

    # __init__ 함수는 C++ 클래스의 생성자와 같은 역할을 한다.
    # self 는 C++의 this 와 같은 역할
    def __init__(self, connection) :
        super(ServerThread, self).__init__()
        self._stop = threading.Event()
        self.connection = connection

    def stop(self):
        self._stop.set()

    def stopped(self):
        return self._stop.isSet()

    def __del__(self) :
        self.stop()
        #self.join()

    def run(self) :
        self.connection.send_message("3team server")

        count = 0
        self.connection.send_message('10')
        for item in self.connection.collection.find() :
            list_str = item['rank'] + '. ' + item['music']
            self.connection.send_message(list_str)
            count += 1
            if count == 10 : break ## 나중에 삭제

        number = int(self.connection.receive_message())

        self.connection.sock.settimeout(10)

        directory_path = "D:/2017_S.W/1st"
        if number is 0:
            self.connection.send_directory(directory_path)

        else:
            number = str(number)
            file_name = self.connection.collection.find({"rank": number})[0]["music"]
            self.connection.send_message(file_name + ".mp3")
            file_name = directory_path + '/' + file_name + ".mp3"
            self.connection.send_file(file_name)

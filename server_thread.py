#coding: utf-8


from pymongo import MongoClient
from TCP_CLASS import *
import threading


class ServerThread(threading.Thread) : # threading.Thread 클래스를 상속 받음

    # __init__ 함수는 C++ 클래스의 생성자와 같은 역할을 한다.
    # self 는 C++의 this 와 같은 역할
    def __init__(self, connection) :
        threading.Thread.__init__(self)
        self.connection = connection

    def run(self) :
        self.connection.send_message( "3team server")
        time.sleep(1)

        msg = ""
        count = 0
        for item in self.connection.collection.find():
            list_str = item['rank'] + '. ' + item['music'] + '\n'
            msg += list_str
            count += 1
            if count == 10: break
        self.connection.send_message(msg)  # 음악리스트를 클라이언트에 전송

        number = self.connection.receive_message()  # 클라이언트가 선택한 번호를 전송받음
        number = int(number)

        self.connection.sock.settimeout(3)

        directory_path = "D:/2017_S.W/1st"
        if number is 0:
            self.connection.send_directory(directory_path)

        else:
            number = str(number)
            file_name = self.connection.collection.find({"rank": number})[0]["music"]
            self.connection.send_message(file_name + ".mp3")
            file_name = directory_path + '/' + file_name + ".mp3"
            self.connection.send_file(file_name)
        sys.exit(0)
#coding: utf-8
from socket import *
from data_crawling import crawling_process
from pymongo import MongoClient
import os
import time
import threading
import Queue

class Crawler_Thread(threading.Thread) :
    def __init__(self) :
        threading.Thread.__init__(self)
        self.__exit = False
        self.folder_idx = 1

    def run(self) :

        while(self.__exit == False) :
            current_time = time.localtime()
            current_minute = current_time.tm_min
            while (current_minute) % 60 == 5 :
                crawling_process(reset = None)
                self.folder_idx = (self.folder_idx + 1) % 2

    def Exit(self) :
        self.__exit = True


class Server_Thread(threading.Thread) :
    def __init__(self, NAME, ADDR) :
        threading.Thread.__init__(self)
        self.__exit = False
        self.CLIENT_NAME = NAME
        self.CLIENT_ADDR = ADDR

    def run(self) :

        MONGO_ADDR = '127.0.0.1:27017'
        connection = MongoClient(MONGO_ADDR)
        db = connection.music_db
        collection = db.music_list

        udpSock.sendto('3 TEAM SERVER', CLIENT_ADDR)
        print CLIENT_NAME + ' 님이 접속 하였습니다.'
        user_input = 'Y'
        while user_input == 'Y':




if __name__ == "__main__" :

    HOST = ''
    PORT = 5001
    ADDR = (HOST, PORT)
    BUFSIZE = 1024 * 10

    folder_list = ["1st", "2nd"]
    thread = Crawler_Thread()
    thread.start()

    udpSock = socket(AF_INET, SOCK_DGRAM)
    udpSock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    udpSock.bind(ADDR)

    while(1) :
        CLIENT_NAME, CLIENT_ADDR = udpSock.recvfrom(BUFSIZE)
        server_thread = Server_Thread(CLIENT_NAME, CLIENT_ADDR)



"""

    file_name = '*.mp3'

    user_input = 'Y'
    file_size = os.path.getsize('D:/2017_S.W/' + file_name)

    while user_input == 'Y' or user_input == 'y' :

        udpSock = socket(AF_INET, SOCK_DGRAM)
        udpSock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        udpSock.bind(ADDR)
        CLIENT_NAME, CLIENT_ADDR = udpSock.recvfrom(BUFSIZE)
        udpSock.sendto('3 TEAM SERVER', CLIENT_ADDR)
        print 'send to ' + CLIENT_NAME

        file = open('D:/2017_S.W/' + file_name, 'rb')

        for line in file :
            udpSock.sendto(line, CLIENT_ADDR)
        udpSock.sendto('EOF', CLIENT_ADDR)
        udpSock.sendto(str(file_size), CLIENT_ADDR)
        user_input, user_addr = udpSock.recvfrom(BUFSIZE)
        print user_input
"""
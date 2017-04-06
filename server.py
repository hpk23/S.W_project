#coding: utf-8
from socket import *

#from data_crawling import crawling_process
from pymongo import MongoClient



if __name__ == "__main__" :

    #os.system("chcp 949")
    #os.system('cls')

    lst = [0, 1]
    print (lst[0:1])

    HOST = ""
    PORT = 5001
    ADDR = (HOST, PORT)
    BUFSIZE = 1024

    folder_list = ["1st", "2nd"]

    #clients = []

    try :
        udpSock = socket(AF_INET, SOCK_DGRAM)
        udpSock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        print ('Socket created')
    except error as msg:
        print ('Failed to create socket. Error Code : ', end = " "); print(str(msg[0], "utf-8"), end = " "); print("Message ", end = " "); print(str(msg[1], "utf-8"))
        sys.exit()

    try :
        udpSock.bind(ADDR)
        print('Bind complete')
    except error as msg :
        print('Bind failed. Error Code : ', end = " "); print(str(msg[0], "utf-8"), end = " "); print("Message ", end = " "); print(str(msg[1], "utf-8"))
        sys.exit()

    while(1) :
        print ("Waiting...")
        CLIENT_NAME, CLIENT_ADDR = udpSock.recvfrom(BUFSIZE)            #  ADDRESS를 받음

        MONGO_ADDR = "127.0.0.1:27017"
        connection = MongoClient(MONGO_ADDR)
        db = connection.music_db
        collection = db.music_list

        udpSock.sendto("3 TEAM SERVER".encode('utf-8'), CLIENT_ADDR)   # 클라이언트에게 응답 메시지 전송
        print(CLIENT_NAME.decode('utf-8'), end=" "); print("님 접속")

        for item in collection.find():
            list_str = item['rank'] + '. ' + item['music']
            udpSock.sendto(list_str.encode('utf-8'), CLIENT_ADDR)   # 클라이언트에게 음악 리스트 메시지 전송
        udpSock.sendto("LIST END".encode('utf-8'), CLIENT_ADDR)     # 클라이언트는 LIST END를 받을때까지 recvfrom

        number, ADDR = udpSock.recvfrom(BUFSIZE)                    # 클라이언트에게 해당하는 음악의 번호를 받음

        number = number.decode('utf-8')

        path = "D:/2017_S.W/S.W_project/1st/"
        file_name = collection.find({"rank" : number})[0]["music"]

        file_name = path + file_name + ".mp3"

        file = open(file_name, "rb")
        lines = file.readlines()

        for line in lines :
            for j in (0, BUFSIZE, BUFSIZE) :
                udpSock.sendto(line[j:j+BUFSIZE], CLIENT_ADDR)    # 클라이언트에게 파일을 BUFSIZE 만큼씩 보냄
        udpSock.sendto("EOF".encode('utf-8'), CLIENT_ADDR)        # 클라이언트는 EOF를 받을때까지 recvfrom
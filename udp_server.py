#coding: utf-8
from udp_functions import *
from pymongo import MongoClient
import hashlib
import time

if __name__ == "__main__" :
    HOST = ""
    PORT = 6009
    ADDR = (HOST, PORT)
    BUFSIZE = 1024 * 10

    udpSock = create_udp_socket(ADDR)

    while (1):
        print ("Waiting...")
        data, addr = receive_message(udpSock, BUFSIZE)
        send_message(udpSock, addr, "3team server")

        MONGO_ADDR = "127.0.0.1:27017"
        connection = MongoClient(MONGO_ADDR)
        db = connection.music_db
        collection = db.music_list

        msg = ""
        for item in collection.find():
            list_str = item['rank'] + '. ' + item['music'] + '\n'
            msg += list_str

        send_message(udpSock, addr, msg) # client 에게 music list 전송
        number, addr = receive_message(udpSock, BUFSIZE)

        path = "D:/2017_S.W/1st/"
        file_name = collection.find({"rank": number})[0]["music"]
        file_name = path + file_name + ".mp3"

        print(file_name.encode('utf-8') + " 파일 전송...")

        hasher = hashlib.sha224()
        with open(file_name, "rb") as f:
            line = f.read()
            line_length = len(line)
            for i in range(0, line_length, BUFSIZE):
                buf = line[i:i + BUFSIZE]
                hasher.update(buf)
                send_message(udpSock, addr, buf)
                time.sleep(0.01)
                #reply, addr = receive_message(udpSock, BUFSIZE)
                #print ('sending buf...'),; print i,;
            #print('clear buf'),;
        send_message(udpSock, addr, "EOF")

        time.sleep(0.5)
        file_size = os.path.getsize(file_name)

        send_message(udpSock, addr, str(file_size))
        reply, addr = receive_message(udpSock, BUFSIZE)
        send_message(udpSock, addr, str(hasher.hexdigest()))
        reply, addr = receive_message(udpSock, BUFSIZE)
        print(file_name.encode('utf-8') + " 파일 전송 완료")
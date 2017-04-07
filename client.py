#coding: utf-8
from socket import *
from functions import *
import os
import re
import codecs
import time
import sys

def create_sock() :
    try :
        sock = socket(AF_INET, SOCK_STREAM)
        sock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    except error as msg:
        print '소켓 생성 실패. Error Code : ',; print str(msg[0]),; print "Message ",; print str(msg[1])
        sys.exit()

    return sock


if __name__ == "__main__" :

    HOST = ''
    PORT = 6001
    ADDR = (HOST, PORT)
    BUFSIZE = 1024*10


    SERVER_HOST = '210.117.182.122'
    SERVER_PORT = 5001
    SERVER_ADDR = (SERVER_HOST, SERVER_PORT)

    csock = create_sock()

    try :
        print "서버에 연결중입니다...\n\n"
        csock.connect(SERVER_ADDR)
    except Exception as e :
        print (e)
        sys.exit()
    data = receive_message(csock, BUFSIZE)
    print(data)

    data = receive_message(csock, BUFSIZE)
    print(data)

    print "번호 입력 : ",
    number = raw_input()
    send_message(csock, number)

    print "전송 받는중..."

    data = receive_message(csock, BUFSIZE)
    out_file = open("temp.mp3", "wb")
    while data != "__END__" :
        if data == "__END__" : print ("같다")
        out_file.write(data)
        data = receive_message(csock, BUFSIZE)
    out_file.close()

    time.sleep(1)

    recv_file_size =receive_message(csock, BUFSIZE)
    hash = receive_message(csock, BUFSIZE)

    hasher = hashlib.sha224()
    with open("temp.mp3", "rb") as f :
        print("hasher")
        buf = f.read()
        hasher.update(buf)

    file_size = os.path.getsize("temp.mp3")

    print str(recv_file_size),; print " :: ",; print str(file_size)

    if str(hasher.hexdigest()) == hash :
        print "같다."
    else :
        print str(hasher.hexdigest()),; print hash

    print "완료"
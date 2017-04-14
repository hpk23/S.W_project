#coding: utf-8
from socket import *
from functions import *
import os
import shutil
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
        sys.exit(1)
    data = receive_message(csock, BUFSIZE) # 서버 응답 메시지
    print(data)

    data = receive_message(csock, BUFSIZE) # 음악 리스트
    print(data)

    print "번호 입력 : ",
    number = raw_input()
    send_message(csock, number)

    print "전송 받는중..."

    out_file = open("temp.mp3", "wb")
    while True :
        data = receive_message(csock, BUFSIZE)
        send_message(csock, "okay")
        if data == "__END__" : break
        out_file.write(data)

    out_file.close()

    original_file_size =receive_message(csock, BUFSIZE)
    hash = receive_message(csock, BUFSIZE)

    hasher = hashlib.sha224()
    with open("temp.mp3", "rb") as f :
        buf = f.read()
        hasher.update(buf)

    recv_file_size = os.path.getsize("temp.mp3")


    if str(hasher.hexdigest()) == hash :
        print "전송완료"
    else :
        print "파일의 해시값이 다릅니다."
        print "원본 파일 크기 : " + str(original_file_size) + " bytes\t받은 파일 크기 : " + str(recv_file_size) + " bytes"
        while(True) :
            print "파일을 지우시겠습니까?(Y/N) : ",
            user_input = raw_input()
            if user_input.upper() != 'Y' and user_input.upper() != 'N' :
                print "잘못 입력 하셨습니다.\n"
                continue

            elif user_input.upper() == 'Y' :
                os.remove("temp.mp3")
                print("파일 삭제 완료")
            break


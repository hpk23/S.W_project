#coding: utf-8
from udp_functions import *
import hashlib


if __name__ == "__main__" :

    HOST = ''
    PORT = 6010
    ADDR = (HOST, PORT)
    BUFSIZE = 1024 * 10


    SERVER_HOST = '210.117.182.122'
    SERVER_PORT = 6009
    SERVER_ADDR = (SERVER_HOST, SERVER_PORT)

    csock = create_udp_socket(ADDR)

    print "이름을 입력해주세요 : ",
    MYNAME = raw_input()
    send_message(csock, SERVER_ADDR, MYNAME)

    reply, addr = receive_message(csock, BUFSIZE) # server로 부터 접속 응답 받음
    print reply

    music_list, addr = receive_message(csock, BUFSIZE)
    print music_list
    print "번호를 입력 해주세요 : ",
    number = raw_input()
    send_message(csock, SERVER_ADDR, number)

    print("전송 받는중...")

    out_file = open("temp.mp3", "wb")
    while True:
        data, addr = receive_message(csock, BUFSIZE)
        if data == "EOF": break
        send_message(csock, SERVER_ADDR, "okay")
        out_file.write(data)
    out_file.close()

    original_file_size, server_addr = receive_message(csock, BUFSIZE)
    hash, server_addr = receive_message(csock, BUFSIZE)

    hasher = hashlib.sha224()
    with open("temp.mp3", "rb") as f:
        buf = f.read()
        hasher.update(buf)

    recv_file_size = os.path.getsize("temp.mp3")

    if str(hasher.hexdigest()) == hash :
        print "전송완료"
        print "원본 파일 크기 : " + str(original_file_size) + " bytes\t받은 파일 크기 : " + str(recv_file_size) + " bytes"
        print "원본 파일 해시값 : " + str(hash) + " 받은 파일 해시값 : " + str(hasher.hexdigest())
    else :
        print "파일의 해시값이 다릅니다."
        print "원본 파일 해시값 : " + str(hash) + " 받은 파일 해시값 : " + str(hasher.hexdigest())
        print "원본 파일 크기 : " + str(original_file_size) + " bytes\t받은 파일 크기 : " + str(recv_file_size) + " bytes"
        while (True) :
            print "파일을 지우시겠습니까?(Y/N) : ",
            user_input = raw_input()
            if user_input.upper() != 'Y' and user_input.upper() != 'N':
                print "잘못 입력 하셨습니다.\n"
                continue

            elif user_input.upper() == 'Y':
                os.remove("temp.mp3")
                print("파일 삭제 완료")
            break

        print("완료")
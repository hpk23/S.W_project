#coding: utf-8
from TCP_CLASS import TcpSocket
from UDP_CLASS import UdpSocket
from server_thread import *
import sys
import time

if __name__ == "__main__" :
    HOST = ""
    PORT = 5005
    ADDR = (HOST, PORT)
    LISTEN_NUMBER = 15
    BUFSIZE = 1024


    while True :
        connection = UdpSocket(PORT, BUFSIZE=BUFSIZE)

        protocol, addr = connection.receive_message()

        if protocol == '0' :
            print "TCP Protocol\n"

            connection = TcpSocket(PORT, SERVER=True, LISTEN_NUMBER=LISTEN_NUMBER, BUFSIZE=BUFSIZE)

            client_sock, addr = connection.accept_sock.accept()
            connection.setClient(client_sock, addr)
            thread = ServerThread(connection)
            thread.run()
            del thread
            continue

        print "UDP Protocol\n"

        # UDP SERVER

        connection.send_message(addr, "3team server")
        time.sleep(1)

        msg = ""
        count = 0
        for item in connection.collection.find():
            list_str = item['rank'] + '. ' + item['music'] + '\n'
            msg += list_str
            count += 1
            if count == 10 : break
        connection.send_message(addr, msg)  #음악리스트를 클라이언트에 전송

        number, addr = connection.receive_message() # 클라이언트가 선택한 번호를 전송받음
        number = int(number)

        #connection.sock.settimeout(3)

        directory_path = "D:/2017_S.W/1st"
        if number is 0 :
            connection.send_directory(addr, directory_path)

        else :
            number = str(number)
            file_name = connection.collection.find({"rank": number})[0]["music"]
            connection.send_message(addr, file_name + ".mp3")
            file_name = directory_path + '/' + file_name + ".mp3"
            connection.send_file(addr, file_name)
        del connection
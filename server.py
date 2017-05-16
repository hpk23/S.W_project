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

        message, addr = connection.receive_message()

        msg = ""
        count = 0
        for item in connection.collection.find():
            list_str = item['rank'] + '. ' + item['music'] + '\n'
            msg += list_str
            count += 1
            if count == 10: break

        connection.send_message(addr, msg)  # 음악리스트를 클라이언트에 전송

        number, addr = connection.receive_message()  # 클라이언트가 선택한 번호를 전송받음
        number = int(number)

        directory_path = "D:/2017_S.W/1st"
        if number is 0:
            connection.send_directory(addr, directory_path)

        else:
            number = str(number)
            file_name = connection.collection.find({"rank": number})[0]["music"]
            #connection.send_message(addr, file_name + ".mp3")

            file_name = directory_path + '/' + file_name + ".mp3"

            file_size = os.path.getsize(file_name)
            connection.send_message(addr, str(file_size))

            if file_size > 1024 * 60 :

                print "TCP Protocol\n"
                connection = TcpSocket(PORT, SERVER=True, LISTEN_NUMBER=LISTEN_NUMBER, BUFSIZE=BUFSIZE)
                client_sock, addr = connection.accept_sock.accept()
                connection.setClient(client_sock, addr)
                connection.send_message(file_name)

                thread = ServerThread(connection, file_name, file_size, number)
                thread.run()
                del thread
                continue

            else :
                print 'UDP Protocol\n'
                connection.send_message(addr, file_name)
                connection.send_file(addr, file_name)
                del connection






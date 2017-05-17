#coding: utf-8
from TCP_CLASS import TcpSocket
from UDP_CLASS import UdpSocket
from server_thread import *
import sys
import time

if __name__ == "__main__" :
    HOST = ""
    UDP_PORT = 6050
    TCP_PORT = 6055
    UDP_ADDR = (HOST, UDP_PORT)
    TCP_ADDR = (HOST, TCP_PORT)
    LISTEN_NUMBER = 15
    BUFSIZE = 1024

    udp_connection = UdpSocket(UDP_PORT, BUFSIZE=BUFSIZE, HOST=HOST)
    udp_connection.setSocket()
    tcp_connection = TcpSocket(TCP_PORT, SERVER=True, LISTEN_NUMBER=LISTEN_NUMBER, BUFSIZE=BUFSIZE, HOST=HOST)
    tcp_connection.setSocket()

    while True :
        client_sock, addr = tcp_connection.accept_sock.accept()
        tcp_connection.setClient(client_sock, addr)

        message, addr = udp_connection.receive_message()
        msg = ""
        count = 0
        for item in udp_connection.collection.find():
            list_str = item['rank'] + '. ' + item['music'] + '\n'
            msg += list_str
            count += 1
            if count == 10: break

        udp_connection.send_message(addr, msg)  # 음악리스트를 클라이언트에 전송

        number, addr = udp_connection.receive_message()  # 클라이언트가 선택한 번호를 전송받음
        number = int(number)

        directory_path = "D:/2017_S.W/1st"
        if number is 0:
            current_path = directory_path.split('/')[-1]
            directory = directory_path.split('/')[-1]

            length = 0
            for path, dirs, files in os.walk(directory_path) :
                for file in files :
                    length += 1

            udp_connection.send_message(addr, str(length))

            for path, dirs, files in os.walk(directory_path) :
                for file in files :
                    current_directory = path.replace('\\', '/').split('/')[-1]
                    if directory != current_directory :
                        directory = current_directory
                        current_path = current_path + '/' + directory

                    file_name = current_path + '/' + file
                    udp_connection.send_message(addr, file_name)

                    send_file_name = path + '/' + file
                    file_size = os.path.getsize(send_file_name)
                    udp_connection.send_message(addr, str(file_size))

                    if file_size > 1024 * 64 :

                        tcp_connection.send_file(send_file_name)
                        #thread = ServerThread(connection, send_file_name, file_size, number)
                        #thread.run()
                        #del thread
                    else :
                        print 'UDP Protocol\n'
                        udp_connection.send_file(addr, send_file_name)


            #connection.send_directory(addr, directory_path)

        else:
            number = str(number)
            file_name = udp_connection.collection.find({"rank": number})[0]["music"]

            file_name = directory_path + '/' + file_name + ".mp3"

            file_size = os.path.getsize(file_name)
            udp_connection.send_message(addr, str(file_size))

            if file_size > 1024 * 60 :

                print "TCP Protocol\n"
                tcp_connection.send_message(file_name)
                thread = ServerThread(tcp_connection, file_name, file_size, number)
                thread.run()
                del thread
                continue

            else :
                print 'UDP Protocol\n'
                udp_connection.send_message(addr, file_name)
                udp_connection.send_file(addr, file_name)






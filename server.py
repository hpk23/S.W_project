#coding: utf-8
from TCP_CLASS import TcpSocket
from UDP_CLASS import UdpSocket
from server_thread import *
import sys
import time

if __name__ == "__main__" :
    HOST = ""
    PORT = 6050
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
            current_path = directory_path.split('/')[-1]
            directory = directory_path.split('/')[-1]

            length = 0
            for path, dirs, files in os.walk(directory_path) :
                for file in files :
                    length += 1

            connection.send_message(addr, str(length))

            for path, dirs, files in os.walk(directory_path) :
                for file in files :
                    current_directory = path.replace('\\', '/').split('/')[-1]
                    if directory != current_directory :
                        directory = current_directory
                        current_path = current_path + '/' + directory

                    file_name = current_path + '/' + file

                    connection.send_message(addr, file_name)

                    send_file_name = path + '/' + file
                    file_size = os.path.getsize(send_file_name)
                    connection.send_message(addr, str(file_size))

                    if file_size > 1024 * 64 :

                        if connection.protocol != "TCP" :
                            connection.sock.shutdown(1)
                            del connection
                            connection = TcpSocket(PORT, SERVER=True, LISTEN_NUMBER=LISTEN_NUMBER, BUFSIZE=BUFSIZE)
                            time.sleep(2)
                            client_sock, addr = connection.accept_sock.accept()
                            connection.setClient(client_sock, addr)

                        connection.send_file(send_file_name)
                        #thread = ServerThread(connection, send_file_name, file_size, number)
                        #thread.run()
                        #del thread
                    else :
                        print 'UDP Protocol\n'
                        connection.send_message(addr, file_name)
                        connection.send_file(addr, file_name)

                    if connection.protocol != "UDP" :
                        del connection
                        connection = UdpSocket(PORT, BUFSIZE=BUFSIZE)


            #connection.send_directory(addr, directory_path)

        else:
            number = str(number)
            file_name = connection.collection.find({"rank": number})[0]["music"]

            file_name = directory_path + '/' + file_name + ".mp3"

            file_size = os.path.getsize(file_name)
            connection.send_message(addr, str(file_size))

            if file_size > 1024 * 60 :

                print "TCP Protocol\n"
                del connection
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






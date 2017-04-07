import time
import hashlib
import sys
import os
from socket import timeout

def send_message(sock, message) :

    try :
        sock.send(message.encode('utf-8'))
    except :
        sock.send(message)

def receive_message(sock, size) :

    try :
        data = sock.recv(size)
        return data
    except  Exception as e :
        print(e)


def receive_file(sock, size) :
    return sock.recv(size)
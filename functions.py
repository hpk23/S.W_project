import time
import hashlib
import sys
import os

def send_message(sock, message) :

    try :
        sock.send(message.encode('utf-8'))
    except :
        sock.send(message)
    time.sleep(0.0001)

def receive_message(sock, size) :
    data = sock.recv(size)
    try :
        return data.decode('utf-8')
    except :
        return data


def receive_file(sock, size) :
    return sock.recv(size)
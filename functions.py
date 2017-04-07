import time
import hashlib
import sys
import os

def send_message(sock, message) :

    try :
        sock.send(message.encode('utf-8'))
    except :
        sock.send(message)
    #time.sleep(0.001)

def receive_message(sock, size) :

    while True :
        data = sock.recv(size)
        if not data : continue
        return data


def receive_file(sock, size) :
    return sock.recv(size)
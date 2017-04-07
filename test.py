#coding: utf-8
import hashlib

hasher = hashlib.sha224()

with open("D:/2017_S.W/1st/창모_(CHANGMO)-마에스트로_(Maestro).mp3".decode('utf-8'), "rb") as f :
    buf = f.read()
    hasher.update(buf)

print(hasher.hexdigest())
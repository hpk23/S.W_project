#coding: utf-8


from pymongo import MongoClient
from functions import *
import threading


class Server_thread(threading.Thread) :

    def __init__(self, ip, port, connection) :
        threading.Thread.__init__(self)
        self.ip = ip
        self.port = port
        self.csock = connection
        MONGO_ADDR = "127.0.0.1:27017"
        connection = MongoClient(MONGO_ADDR)
        self.db = connection.music_db
        self.collection = self.db.music_list
        self.BUFSIZE = 1024 * 10
        self.client_info = str(self.ip) + ":" + str(self.port)

    def run(self) :

        try :
            self.csock.send("소개발 3조 서버입니다.")

            item_list = self.collection.find()
            msg = ""
            for item in item_list :
                message = item["rank"] + ". " + item["artist"] + " - " + item["title"] + "\n" # 음악 리스트를 클라이언트에 전송
                msg += message
                #send_message(self.csock, message)
            send_message(self.csock, msg)
            #send_message(self.csock, "__END__")
            number = receive_message(self.csock, self.BUFSIZE)

            path = "D:/2017_S.W/1st/"
            file_name = path + self.collection.find({"rank" : number})[0]["music"] + ".mp3"

            print(self.client_info + " 에게 " + file_name.split('/')[-1].encode('utf-8') + " 파일을 전송합니다...")

            hasher = hashlib.sha224()
            with open(file_name, "rb") as f :
                line = f.read()
                for i in range(0, len(line), self.BUFSIZE) :
                    buf = line[i:i+self.BUFSIZE]
                    hasher.update(buf)
                    send_message(self.csock, buf)
                    reply = receive_message(self.csock, self.BUFSIZE)
            send_message(self.csock, "__END__")

            time.sleep(0.5)
            file_size = os.path.getsize(file_name)
            send_message(self.csock, str(file_size)) # 파일 크기
            send_message(self.csock, str(hasher.hexdigest())) # 해쉬값
            print(self.client_info + " 에게 " + file_name.split('/')[-1].encode('utf-8') + " 파일 전송 완료\n\n")
        except Exception as e :
            print self.client_info + " 와의 연결중 예기치 못한 에러가 발생했습니다." + self.client_info + " 와의 접속을 종료합니다...\n\n"
            print(e)
            self.csock.close()
            sys.exit(1)

        sys.exit(0)


        #self.csock.close()
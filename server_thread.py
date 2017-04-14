#coding: utf-8


from pymongo import MongoClient
from functions import *
import threading


class Server_thread(threading.Thread) : # threading.Thread 클래스를 상속 받음

    # __init__ 함수는 C++ 클래스의 생성자와 같은 역할을 한다.
    # self 는 C++의 this 와 같은 역할
    def __init__(self, ip, port, connection) :  
        threading.Thread.__init__(self)
        self.ip = ip
        self.port = port
        self.csock = connection

        # MongoDB에 저장되어있는 MUSIC LIST를 가져오기 위해, MongoDB와의 연결을 위한 객체들을 생성
        # collection은 mysql의 table과 비슷함 (mysql은 database->table에 내가 원하는 항목을 insert, MongoDB는 (database->collection에 내가 원하는 항목을 insert)
        MONGO_ADDR = "127.0.0.1:27017"
        db_connect = MongoClient(MONGO_ADDR) 
        self.db = db_connect.music_db
        self.collection = self.db.music_list
        self.BUFSIZE = 1024 * 10
        self.client_info = str(self.ip) + ":" + str(self.port)

    def run(self) :

        try :
            # client와의 연결 성공시 client에게 메시지를 보냄
            send_message(self.csock, "소개발 3조 서버입니다.")

            # __init__에서 생성한 collection 객체를 이용해 music_list를 불러온다. ( mysql : select * from table ) (MongoDB : collection.find() )
            item_list = self.collection.find()
            msg = ""

            # msg 변수에 collection에서 가져온 rank. artist - title 을 붙여 msg 변수에 대입 한 뒤 한번에 client에게 보낸다.
            for item in item_list :
                message = item["rank"] + ". " + item["artist"] + " - " + item["title"] + "\n"
                msg += message
            send_message(self.csock, msg)

            # client는 위에서 보낸 music_list를 보고 받고 싶은 음악의 번호를 입력해 server에 보내게됨
            number = receive_message(self.csock, self.BUFSIZE) # number : client에서 보낸 음악의 번호

            path = "D:/2017_S.W/1st/"

            # MongoDB의 collection에서 client가 보낸 번호를 가진 항목을 찾아서 파일 이름을 가져옴
            file_name = path + self.collection.find({"rank" : number})[0]["music"] + ".mp3"

            print(self.client_info + " 에게 " + file_name.split('/')[-1].encode('utf-8') + " 파일을 전송합니다...")

            # hashlib에 있는 sha224 해시를 하기 위한 변수
            hasher = hashlib.sha224()

            # file을 binary 로 읽어 들이고 pointer의 이름을 f로 지정함
            with open(file_name, "rb") as f :
                # f.read는 file의 한 line을 읽어들임
                line = f.read() 
                # i=0 to line의길이, i += BUFSIZE
                for i in range(0, len(line), self.BUFSIZE) : 
                    # buf에 line[i] 부터 line[i+BUFSIZE-1] 까지의 문자를 대입 
                    buf = line[i:i+self.BUFSIZE] 
                    # 읽어들인 buf에 해시 적용
                    hasher.update(buf) 
                    # buf를 client에게 보냄
                    send_message(self.csock, buf)
                    # client에서 해당 buf를 잘 받았다는 message를 받음
                    reply = receive_message(self.csock, self.BUFSIZE)
            # 파일 전송이 끝났다는 message를 보냄
            send_message(self.csock, "__END__")

            # 0.5초간 대기
            time.sleep(0.5)

            # 방금 보낸 파일의 크기를 구함
            file_size = os.path.getsize(file_name)
            # 방금 보낸 파일의 크기를 client에게 보냄
            send_message(self.csock, str(file_size)) # 파일 크기
            # 방금 보낸 파일의 해시값을 client에게 보냄
            send_message(self.csock, str(hasher.hexdigest())) # 해쉬값
            print(self.client_info + " 에게 " + file_name.split('/')[-1].encode('utf-8') + " 파일 전송 완료\n\n")
        except Exception as e :
            print self.client_info + " 와의 연결중 예기치 못한 에러가 발생했습니다." + self.client_info + " 와의 접속을 종료합니다...\n\n"
            print(e)
            self.csock.close()
            sys.exit(1)

        sys.exit(0)
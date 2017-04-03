#coding: utf-8
from bs4 import BeautifulSoup
from pymongo import MongoClient
import youtube_dl
import urllib
import re
import pymongo
import glob
import shutil

def collection_reset(db, collection) :
    collection.drop()
    db.create_collection("music_list")
    collection = db.music_list
    collection.create_index([("music", pymongo.ASCENDING)], unique=True)

def collection_insert(collection, rank, artist, title) :
    insert_item = {"rank" : rank, "artist" : artist, "title" : title, "music" : artist.strip() + '-' + title.strip()}
    collection.insert(insert_item)

def collection_remove(collection, artist, title) :
    music = artist.strip() + '-' + title.strip()
    collection.remove({"music" : music})

def search_url(artist, title):
    search_word = artist.encode('utf-8') + '-' + title.encode('utf-8')
    query_url = "https://www.youtube.com/results?search_query={}".format(search_word)
    ret = None

    print query_url

    try:
        html_text = urllib.urlopen(query_url).read()
    except:
        print 'urlopen fail'
        return
    soup = BeautifulSoup(html_text, "html.parser")
    atags = soup.findAll('a', href=True, title=True)
    for atag in atags :
        if atag.get('class')[0] != 'yt-uix-tile-link' :
            continue
        if ret is None :
            ret = re.findall(r'^/watch\?v=.+', atag["href"])

        for filter in video_filters :
            if atag.get('title').find(filter) != -1 :
                ret = re.findall(r'^/watch\?v=.+', atag["href"])
                print "https://www.youtube.com" + ret[0]
                return "https://www.youtube.com" + ret[0]

    print "https://www.youtube.com" + ret[0]
    return "https://www.youtube.com" + ret[0]

def download_music(music_url, artist, title, rank) :
    ydl_opts = {
        'format': 'bestaudio/best',

        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }

    urls = [music_url]

    try :
        with youtube_dl.YoutubeDL(ydl_opts) as ydl :
            ydl.download(urls)
    except :
        print 'download_error'

if __name__ == "__main__" :

    video_filters = ['Official Audio', '[MV]', 'M/V', '[Audio]', u'듣기', 'Full ver', 'Music Video', '[MP3 Audio]']

    MONGO_ADDR = '127.0.0.1'
    connection = MongoClient(MONGO_ADDR)
    db = connection.music_db
    collection = db.music_list

    collection_reset(db, collection) ####### collection reset

    urls = ['http://www.genie.co.kr/chart/top100?ditc=D&ymd=20170331&hh=15&rtm=Y&pg=1',
           'http://www.genie.co.kr/chart/top100?ditc=D&ymd=20170331&hh=15&rtm=Y&pg=2']

    for url in urls :
        html_text = urllib.urlopen(url).read() # 해당 url의 html text를 얻어옴
        soup = BeautifulSoup(html_text, 'html.parser')

        lst = []
        for item in soup.find_all('div') :
            class_name = item.get('class')
            find_string = re.compile('rank-\d')  # 정규표현식 \d : 숫자와 매칭
            if class_name is None or len(class_name) < 2 : continue
            if re.match(find_string, class_name[1]) :
                music_info = item.find_all('span')
                rank = music_info[0].text.strip().strip('\n')
                atags = music_info[1].find_all('a')
                music_name = atags[2].text
                artist = atags[3].text

                try :
                    #collection_remove(collection, artist, music_name)
                    collection_insert(collection, rank, artist, music_name)
                except :
                    print rank, ' : ', music_name, '-', artist
                    continue

                download_url = search_url(artist, music_name)
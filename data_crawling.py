#coding: utf-8
from __future__ import unicode_literals
from bs4 import BeautifulSoup
from pymongo import MongoClient
import youtube_dl
import urllib
import re
import sys
import pymongo
import glob
import shutil

def collection_show_data(collection) :
    for item in collection.find() :
        print (item['music'])

def collection_reset(db, collection) :
    collection.drop()
    db.create_collection("music_list")
    collection = db.music_list
    collection.create_index([("music", pymongo.ASCENDING)], unique=True)

def collection_insert(collection, rank, artist, title) :
    insert_item = {"rank" : rank.strip(), "artist" : artist.strip(), "title" : title.strip(), "music" : artist.strip() + '-' + title.strip()}
    collection.insert(insert_item)

def collection_remove(collection, artist, title) :
    music = artist.strip() + '-' + title.strip()
    collection.remove({"music" : music})

def search_url(artist, title):
    video_filters = ['Official Audio', '[MV]', 'M/V', u'듣기', 'Full ver', 'Music Video', '[MP3 Audio]']

    search_word = artist + '-' + title

    query_url = "https://www.youtube.com/results?search_query={}".format(search_word)
    ret = None

    try:
        html_text = urllib.urlopen(query_url).read()
    except Exception as e :
        print 'url open error : ',; print e
        sys.exit(1)
    soup = BeautifulSoup(html_text, "lxml")
    atags = soup.findAll('a', href=True, title=True)
    for atag in atags :
        if atag.get('class')[0] != 'yt-uix-tile-link' :
            continue
        if ret is None :
            ret = re.findall(r'^/watch\?v=.+', atag["href"])

        for filter in video_filters :
            if atag.get('title').find(filter) != -1 :
                ret = re.findall(r'^/watch\?v=.+', atag["href"])
                print ("https://www.youtube.com" + ret[0])
                return "https://www.youtube.com" + ret[0]

    print ("https://www.youtube.com" + ret[0])
    return "https://www.youtube.com" + ret[0]

def download_music(music_url, rank, artist, title, collection) :

    rank = re.sub('\s', '', rank.strip())
    artist = re.sub('\s', '_', artist.strip())
    title = re.sub('\s', '_', title.strip())
    file_name = artist + '-' + title + '.mp3'
    #file_name = artist + '-' + title + '.mp3'
    ydl_opts = {
        'format': 'bestaudio/best',
        #'outtmpl' : 'd:/2017_S.W/S.W_project/1st/{}'.format(file_name),

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

        file_path = 'd:/2017_S.W/S.W_project/*.mp3'
        for path in glob.glob(file_path) :
            dst_path = 'd:/2017_S.W/1st/' + file_name
            shutil.move(path, dst_path)
        collection_insert(collection, rank, artist, title)

    except Exception as e:
        print ('download_error or music exist')
        print (e)

def crawling_process(reset=None) :

    MONGO_ADDR = '127.0.0.1:27017'
    connection = MongoClient(MONGO_ADDR)
    db = connection.music_db
    collection = db.music_list

    if reset is not None :
        collection_reset(db, collection)

    urls = ['http://www.genie.co.kr/chart/top100?ditc=D&ymd=20170331&hh=15&rtm=Y&pg=1',
            'http://www.genie.co.kr/chart/top100?ditc=D&ymd=20170331&hh=15&rtm=Y&pg=2']

    for url in urls:
        html_text = request.urlopen(url).read()

        soup = BeautifulSoup(html_text, 'lxml')

        lst = []
        for item in soup.find_all('div'):
            class_name = item.get('class')
            find_string = re.compile('rank-\d')  # 정규표현식 \d : 숫자와 매칭
            if class_name is None or len(class_name) < 2: continue
            if re.match(find_string, class_name[1]):
                music_info = item.find_all('span')
                rank = music_info[0].text.strip().strip('\n')
                atags = music_info[1].find_all('a')
                music_name = atags[2].text
                artist = atags[3].text

                try:
                    download_url = search_url(artist, music_name)
                    download_music(download_url, rank, artist, music_name, collection)

                except:
                    #print ('Exception : ', rank, '. ', artist, '-', music_name)
                    continue

    print ('Done')

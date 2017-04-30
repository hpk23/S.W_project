#coding: utf-8
from __future__ import unicode_literals
from bs4 import BeautifulSoup
import youtube_dl
import urllib
import re
import sys
import pymongo
import glob
import shutil

def search_url(artist, title):
    video_filters = ['Official Audio', '[MV]', 'M/V', u'듣기', 'Full ver', 'Music Video', '[MP3 Audio]']

    search_word = artist + '-' + title

    query_url = "https://www.youtube.com/results?search_query={}".format(search_word).decode('utf-8')
    ret = None

    try:
        html_text = urllib.urlopen(query_url).read()
    except Exception as e:
        print 'url open error : ', ;
        print e
        sys.exit(1)
    soup = BeautifulSoup(html_text, "lxml")
    atags = soup.findAll('a', href=True, title=True)
    for atag in atags:
        if atag.get('class')[0] != 'yt-uix-tile-link':
            continue
        if ret is None:
            ret = re.findall(r'^/watch\?v=.+', atag["href"])

        for filter in video_filters:
            if atag.get('title').find(filter) != -1:
                ret = re.findall(r'^/watch\?v=.+', atag["href"])
                print ("https://www.youtube.com" + ret[0])
                return "https://www.youtube.com" + ret[0]

    print ("https://www.youtube.com" + ret[0])
    return "https://www.youtube.com" + ret[0]


def download_music(music_url, artist, title):
    # re.sub(pattern, string) pattern : 1) \s - 모든 공백을 지움
    out_file = open('music_genre.txt', 'a')

    artist = re.sub('\s', '_', artist.strip())
    title = re.sub('\s', '_', title.strip())
    file_name = artist + '-' + title + '.mp3'
    # file_name = artist + '-' + title + '.mp3'
    ydl_opts = {
        'format': 'bestaudio/best',
        # 'outtmpl' : 'd:/2017_S.W/S.W_project/1st/{}'.format(file_name),

        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }

    urls = [music_url]

    try:
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            ydl.download(urls)

        file_path = 'd:/2017_S.W/S.W_project/*.mp3'
        for path in glob.glob(file_path):
            dst_path = 'd:/2017_S.W/genre/hiphop/' + file_name
            shutil.move(path, dst_path)

        out_file.write(file_name + ' 1\n')  # 1: hiphop

    except Exception as e:
        print ('download_error or music exist')
        print (e)


def crawling_process(reset=None):

    hiphop_urls = ['http://www.genie.co.kr/genre/L0104?genreCode=L0104&pg=1',
                   'http://www.genie.co.kr/genre/L0104?genreCode=L0104&pg=2',
                   'http://www.genie.co.kr/genre/L0104?genreCode=L0104&pg=3']

    for url in hiphop_urls:
        html_text = urllib.urlopen(url).read()

        soup = BeautifulSoup(html_text, 'lxml')

        lst = []
        for item in soup.find_all('div'):
            class_name = item.get('class')
            find_string = re.compile('list')  # 정규표현식 \d : 숫자와 매칭
            if class_name is None : continue

            if re.match(find_string, class_name[0]):
                music_info = item.find_all('span')
                atags = music_info[1].find_all('a')
                music_name = atags[2].text
                artist = atags[3].text

                try:
                    pass
                    download_url = search_url(artist, music_name)
                    download_music(download_url, artist, music_name)

                except:
                    # print ('Exception : ', rank, '. ', artist, '-', music_name)
                    continue

    print ('Done')


crawling_process()
#coding: utf-8
from bs4 import BeautifulSoup
import urllib
import re

if __name__ == "__main__" :

    urls = ['http://www.genie.co.kr/chart/top100?ditc=D&ymd=20170331&hh=15&rtm=Y&pg=1',
           'http://www.genie.co.kr/chart/top100?ditc=D&ymd=20170331&hh=15&rtm=Y&pg=2']

    for url in urls :
        html_text = urllib.urlopen(url).read()
        soup = BeautifulSoup(html_text, 'html.parser')

        lst = []
        for item in soup.find_all('div') :
            class_name = item.get('class')#
            find_string = re.compile('rank-\d')  #\d : 숫자와 매칭
            if class_name is None or len(class_name) < 2 : continue
            if re.match(find_string, class_name[1]) :
                music_info = item.find_all('span')
                rank = music_info[0].text.strip().strip('\n')
                atags = music_info[1].find_all('a')
                music_name = atags[2].text
                artist = atags[3].text
                print rank, ' : ', music_name, '-', artist


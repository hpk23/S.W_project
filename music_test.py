#coding: cp949
import numpy as np
import soundfile as sf


file_name = u"Red_Velvet_(레드벨벳)-Rookie.wav"

if type(file_name) == type(u'') :
       file_name = file_name.encode('euc-kr').decode('cp949')
       print 'type '

print file_name

f = sf.SoundFile(file_name)
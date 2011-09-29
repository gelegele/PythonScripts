# coding: utf-8
'''
東京電力APIを利用した電力使用量メーター
'''
import urllib
import json
import time
import calendar

#JSONデータの取得
res = urllib.urlopen("http://tepco-usage-api.appspot.com/latest.json")
map = json.load(res.fp)

#UTC時刻をJST時刻に変換
entryfor = map.get('entryfor')
utcTime = time.strptime(entryfor, "%Y-%m-%d %H:%M:%S")
jstTime = time.localtime(calendar.timegm(utcTime))
hour = str(jstTime.tm_hour)
if len(hour) == 1:
    hour = '0' + hour  #０づめ
min = str(jstTime.tm_min)
if len(min) == 1:
    min = '0' + min

percentage = map.get('usage') * 1.0 / map.get('capacity') * 1.0 * 100  #商の小数点以下算出のために1.0掛けが必要
percentage = str(round(percentage)).split('.')[0]

print '電力使用量 ' + hour + '時' + min + '分' + ' ' + percentage + '%'


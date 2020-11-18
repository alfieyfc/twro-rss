# TODO: 
# - refactor write to file
# - refactor broadcast news
# - fix scenario: old post move to top
# -*- coding: utf-8 -*-
import requests, os, sys

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)

URL = 'https://api.line.me/v2/bot/message/broadcast'
  
def main():
    import json
    import datetime
    import os
    import argparse
    try:
        token = os.environ['LINE_TOKEN']
    except KeyError:
        sys.exit('LINE_TOKEN is not defined!')

    line_bot_api = LineBotApi(token)

    parser = argparse.ArgumentParser(
        description='Send a LINE Notify message, possibly with an image.')
    parser.add_argument('--img_file', help='the image file to be sent')
    parser.add_argument('--m', help='extra message')
    args = parser.parse_args()

    res = requests.post('https://ro.gnjoy.com.tw/api/getNewsList.ashx', data='pageSize=20&GameId=RO', headers={'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8', 'x-requested-with': 'XMLHttpRequest' }).json()

    oldNews = []
    oldNewsIds = []
    latest = 0
    count = 0
    with open('/data/news_record.txt', 'r') as f:
    # with open('news_record.txt', 'r') as f:
      oldNews = f.readlines()
      if(len(oldNews) > 0):
        for i in range(len(oldNews)):
          oldNewsIds.append(oldNews[i].split()[0])

    print(oldNewsIds)
    oldNewsId=0
    for i in range(20):
      try:
        oldNewsId = oldNewsIds.index(str(res['news'][i]['newsId']))
      except ValueError as identifier:
        print(identifier, end="; ")
        oldNewsId = i
      if i > oldNewsId:
        count -= 1
      print("oldNewsId=("+str(oldNewsId)+"), i=("+str(i)+"), count=("+str(count)+")")

    with open('/data/news_record.txt', 'w+') as f:
    # with open('news_record.txt', 'w+') as f:
      for i in range(20):
        newsId = res['news'][i]['newsId']
        print("newsId=" + str(newsId), end ="; ")

        if (str(newsId) not in oldNewsIds):
          print("News discovered!", end=" ")
          # write to file
          s = int(res['news'][i]['publish_date'][6:19]) / 1000
          date = datetime.datetime.fromtimestamp(s)
          entry = str(res['news'][i]['newsId']).ljust(6) + str(date).ljust(24) + res['news'][i]['newsTitle']
          f.write(entry + "\n")
          # broadcast news
          message = "仙境傳說公告\n" + res['news'][i]['newsTitle'] + "\n" + str(date)
          message += "\nhttps://ro.gnjoy.com.tw/notice/notice_view.aspx?id=" + str(res['news'][i]['newsId'])
          # Push Notification
          status_code = line_bot_api.broadcast(TextSendMessage(text=message))
          print('Message broadcasted!')
          print('status_code = {}'.format(status_code))
          count += 1

        else:
          print("Old post...", end ="; ")

          # In case unexpected TypeError
          try:
            oldNewsIndex = oldNewsIds.index(str(newsId))
          except ValueError as identifier:
            print(identifier)
            continue;

          if oldNewsIndex + count > i:
            print("But updated! oldNewsIndex=(" + str(oldNewsIndex + count) + "), i=(" + str(i) +")", end="; ")
            # write to file
            s = int(res['news'][i]['publish_date'][6:19]) / 1000
            date = datetime.datetime.fromtimestamp(s)
            entry = str(res['news'][i]['newsId']).ljust(6) + str(date).ljust(24) + res['news'][i]['newsTitle']
            f.write(entry + "\n")
            # broadcast news
            message = "仙境傳說公告\n" + res['news'][i]['newsTitle'] + "\n" + str(date)
            message += "\nhttps://ro.gnjoy.com.tw/notice/notice_view.aspx?id=" + str(res['news'][i]['newsId'])
            # Push Notification
            status_code = line_bot_api.broadcast(TextSendMessage(text=message))
            print('Message broadcasted!')
            print('status_code = {}'.format(status_code))
            
          else:
            print("")
            # write to file
            s = int(res['news'][i]['publish_date'][6:19]) / 1000
            date = datetime.datetime.fromtimestamp(s)
            entry = str(res['news'][i]['newsId']).ljust(6) + str(date).ljust(24) + res['news'][i]['newsTitle']
            f.write(entry + "\n")        
  
if __name__ == '__main__':
    main()
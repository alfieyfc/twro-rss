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

    rec = []
    latest = 0
    with open('/data/news_record.txt', 'r') as f:
      rec = f.readlines()
      if(len(rec) > 0):
        for i in range(len(rec)):
          current = rec[i].split()[0]
          if int(latest) < int(current):
            latest = current

    with open('/data/news_record.txt', 'w+') as f:
      for i in range(20):
        id = res['news'][i]['newsId']
        print("id=" + str(id) + "; latest_record=" + str(latest))
        if int(id) <= int(latest):
          print("Not news...")
          continue;
        
        s = int(res['news'][i]['publish_date'][6:19]) / 1000
        date = datetime.datetime.fromtimestamp(s)
        entry = str(res['news'][i]['newsId']).ljust(6) + str(date).ljust(24) + res['news'][i]['newsTitle']
        f.write(entry + "\n")
        message = "仙境傳說公告\n" + res['news'][i]['newsTitle'] + "\n" + str(date)
        message += "\nhttps://ro.gnjoy.com.tw/notice/notice_view.aspx?id=" + str(res['news'][i]['newsId'])

        # Push Notification
        status_code = line_bot_api.broadcast(TextSendMessage(text=message))
        print('Message broadcasted!')
        print('status_code = {}'.format(status_code))
        
        if(len(rec) > 0):
          rec = rec[:-1]

      for line in rec:
        f.write(line)
  
if __name__ == '__main__':
    main()
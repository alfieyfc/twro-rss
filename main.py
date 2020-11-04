# -*- coding: utf-8 -*-

import requests
import importlib
import sys
importlib.reload(sys)

URL = 'https://notify-api.line.me/api/notify'
  
def send_message(token, msg, img=None):
    """Send a LINE Notify message (with or without an image)."""
    headers = {'Authorization': 'Bearer ' + token}
    payload = {'message': msg}
    files = {'imageFile': open(img, 'rb')} if img else None
    r = requests.post(URL, headers=headers, params=payload, files=files)
    if files:
        files['imageFile'].close()
    return r.status_code
  
def main():
    import json
    import datetime
    import os
    import argparse
    try:
        token = os.environ['LINE_TOKEN']
    except KeyError:
        sys.exit('LINE_TOKEN is not defined!')

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
        latest = rec[0].split()[0]

    with open('/data/news_record.txt', 'w+') as f:
      for i in range(20):
        id = res['news'][i]['newsId']
        if int(id) <= int(latest):
          break;
        
        s = int(res['news'][i]['publish_date'][6:19]) / 1000
        date = datetime.datetime.fromtimestamp(s)
        entry = str(res['news'][i]['newsId']).ljust(6) + str(date).ljust(24) + res['news'][i]['newsTitle']
        f.write(entry + "\n")
        message = "仙境傳說公告\n" + res['news'][i]['newsTitle'] + "\n" + str(date)
        message += "\nhttps://ro.gnjoy.com.tw/notice/notice_view.aspx?id=" + str(res['news'][i]['newsId'])

        # Push Notification
        status_code = send_message(token, message, args.img_file)
        print('status_code = {}'.format(status_code))
        
        if(len(rec) > 0):
          rec = rec[:-1]

      for line in rec:
        f.write(line)
  
if __name__ == '__main__':
    main()